#!/bin/bash

# Enable strict mode
set -euo pipefail

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

# Function to validate inputs
validate_inputs() {
    if [[ -z "${INPUT_CONDITIONS:-}" ]]; then
        print_error "CONDITIONS input is required"
    fi
    if [[ -z "${INPUT_TRUE_VALUES:-}" ]]; then
        print_error "TRUE_VALUES input is required"
    fi
    if [[ -z "${INPUT_FALSE_VALUES:-}" ]]; then
        print_error "FALSE_VALUES input is required"
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
            print_debug "Warning: Variable $varname is not set"
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
        print_error "Number of conditions, true values, and false values must match"
    }
    
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
        
        # Set the output
        local output_name="output_$((i + 1))"
        printf "%s=%s\n" "$output_name" "$result"
        printf "%s=%s\n" "$output_name" "$result" >> "$GITHUB_OUTPUT"
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
}

# Execute main function with error handling
if ! main; then
    print_error "Script execution failed"
fi