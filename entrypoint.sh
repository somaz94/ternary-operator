#!/bin/bash

# Enable strict mode, but allow for unbound variables
set -eo pipefail

# Function to print headers
print_header() {
    printf "\n%s\n" "=================================================="
    printf "🚀 %s\n" "$1"
    printf "%s\n\n" "=================================================="
}

# Function to print debug messages
print_debug() {
    printf "🔍 Debug: %s\n" "$1"
}

# Function to print error messages
print_error() {
    printf "❌ Error: %s\n" "$1"
    exit 1
}

# Function to print success messages
print_success() {
    printf "✅ Success: %s\n" "$1"
}

# Function to safely write output
safe_write_output() {
    local key="$1"
    local value="$2"
    printf "%s=%s\n" "$key" "$value"
    if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
        printf "%s=%s\n" "$key" "$value" >> "$GITHUB_OUTPUT"
    fi
}

# Function to validate inputs
validate_inputs() {
    local missing_inputs=()
    [[ -z "${INPUT_CONDITIONS:-}" ]] && missing_inputs+=("CONDITIONS")
    [[ -z "${INPUT_TRUE_VALUES:-}" ]] && missing_inputs+=("TRUE_VALUES")
    [[ -z "${INPUT_FALSE_VALUES:-}" ]] && missing_inputs+=("FALSE_VALUES")
    
    if [[ ${#missing_inputs[@]} -gt 0 ]]; then
        print_error "Missing required inputs: ${missing_inputs[*]}"
    fi

    # Add maximum condition check
    IFS=',' read -ra conditions <<< "$INPUT_CONDITIONS"
    if [[ ${#conditions[@]} -gt 10 ]]; then
        print_error "Maximum number of conditions (10) exceeded. Found ${#conditions[@]} conditions"
    fi
}

# Function to get variable value
get_var_value() {
    local varname="$1"
    if [[ -n "${!varname:-}" ]]; then
        printf '%s' "${!varname}"
    else
        print_debug "Warning: Variable $varname is not set or empty"
        printf ''
    fi
}

# Function to evaluate conditions and set outputs
evaluate_conditions() {
    local -a conditions true_values false_values
    IFS=',' read -ra conditions <<< "$INPUT_CONDITIONS"
    IFS=',' read -ra true_values <<< "$INPUT_TRUE_VALUES"
    IFS=',' read -ra false_values <<< "$INPUT_FALSE_VALUES"
    
    if [[ ${#conditions[@]} -ne ${#true_values[@]} ]] || [[ ${#conditions[@]} -ne ${#false_values[@]} ]]; then
        print_error "Number of conditions (${#conditions[@]}), true values (${#true_values[@]}), and false values (${#false_values[@]}) must match"
    fi
    
    print_debug "Processing ${#conditions[@]} conditions"
    
    for i in "${!conditions[@]}"; do
        local condition="${conditions[i]}"
        printf "\n📋 Evaluating Condition %d: %s\n" "$((i + 1))" "$condition"
        
        # Replace variables in condition
        local processed_condition="$condition"
        for varname in $(echo "$condition" | grep -oE '\b[A-Z_]+\b'); do
            local value=$(get_var_value "$varname")
            if [[ -n "$value" ]]; then
                print_debug "Variable $varname = $value"
                processed_condition="${processed_condition//$varname/\"$value\"}"
            fi
        done
        
        print_debug "Processed condition: $processed_condition"
        
        # Evaluate the condition
        local result
        if eval "test $processed_condition" 2>/dev/null; then
            result="${true_values[i]}"
            print_success "Condition $((i + 1)) is TRUE"
        else
            result="${false_values[i]}"
            print_debug "Condition $((i + 1)) is FALSE"
        fi
        
        safe_write_output "output_$((i + 1))" "$result"
    done
}

# Main execution
main() {
    print_header "Condition Evaluator"
    
    print_debug "Starting validation"
    validate_inputs
    
    print_debug "Starting condition evaluation"
    evaluate_conditions
    
    print_header "Process Completed Successfully"
    return 0
}

# Execute main function
if ! main; then
    print_error "Script execution failed"
fi