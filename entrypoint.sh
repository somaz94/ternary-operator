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
    printf "✅ %s\n" "$1"
}

# Function to safely write to GITHUB_OUTPUT
safe_write_output() {
    local key="$1"
    local value="$2"
    
    # Print to stdout for debugging
    printf "%s=%s\n" "$key" "$value"
    
    # Write to GITHUB_OUTPUT if it exists
    if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
        printf "%s=%s\n" "$key" "$value" >> "$GITHUB_OUTPUT"
    else
        print_debug "GITHUB_OUTPUT not set, skipping GitHub Actions output"
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
}

# Function to replace variable placeholders with their actual values
replace_placeholders() {
    local condition="$1"
    print_debug "Processing condition: $condition"
    
    for varname in $(echo "$condition" | grep -oE '\b[A-Z_]+\b'); do
        if [[ -n "${!varname:-}" ]]; then
            local value="${!varname}"
            print_debug "Variable $varname = $value"
            
            # Enhanced escaping for special characters
            local escaped_value
            escaped_value=$(printf '%s' "$value" | sed 's/[\/&"'\'']/\\&/g')
            
            # Replace the variable name with its escaped value
            condition="${condition//$varname/$escaped_value}"
        else
            print_debug "Warning: Variable $varname is not set or empty"
        fi
    done
    
    print_debug "Processed condition: $condition"
    printf '%s' "$condition"
}

# Function to evaluate conditions and set outputs
evaluate_conditions() {
    local -a conditions true_values false_values
    IFS=',' read -ra conditions <<< "$INPUT_CONDITIONS"
    IFS=',' read -ra true_values <<< "$INPUT_TRUE_VALUES"
    IFS=',' read -ra false_values <<< "$INPUT_FALSE_VALUES"
    
    # Validate array lengths match
    if [[ ${#conditions[@]} -ne ${#true_values[@]} ]] || [[ ${#conditions[@]} -ne ${#false_values[@]} ]]; then
        print_error "Number of conditions (${#conditions[@]}), true values (${#true_values[@]}), and false values (${#false_values[@]}) must match"
    fi
    
    print_debug "Processing ${#conditions[@]} conditions"
    
    for i in "${!conditions[@]}"; do
        printf "\n📋 Evaluating Condition %d:\n" "$((i + 1))"
        print_debug "Original condition: ${conditions[i]}"
        
        # Process the condition
        local dynamic_condition
        dynamic_condition=$(replace_placeholders "${conditions[i]}")
        print_debug "Processed condition: $dynamic_condition"
        
        # Evaluate the condition
        local result
        if eval "[[ $dynamic_condition ]]" 2>/dev/null; then
            result="${true_values[i]}"
            print_success "Condition $((i + 1)) evaluated to true"
        else
            result="${false_values[i]}"
            print_debug "Condition $((i + 1)) evaluated to false"
        fi
        
        # Set the output using safe write function
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

# Execute main function with error handling
if ! main; then
    print_error "Script execution failed"
fi