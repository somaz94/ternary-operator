#!/bin/bash

# Allow git operations in the current directory
git config --global --add safe.directory /usr/src

# Explicitly set safe directory for git operations
git config --global --add safe.directory /github/workspace

echo "Debug: Starting script execution."

IFS=',' read -ra conditions <<< "$(echo $INPUT_CONDITIONS)"
IFS=',' read -ra true_values <<< "$(echo $INPUT_TRUE_VALUES)"
IFS=',' read -ra false_values <<< "$(echo $INPUT_FALSE_VALUES)"

# Function to replace variable placeholders with their actual values
function replace_placeholders {
    local condition="$1"
    for varname in $(echo "$condition" | grep -oE '\b[A-Z_]+\b'); do
        local value="${!varname}"
        condition=$(echo "$condition" | sed "s/\b$varname\b/$value/g")
    done
    echo "$condition"
}

# Loop through the conditions and evaluate them
for i in "${!conditions[@]}"; do
    echo "Debug: Evaluating condition $i - ${conditions[i]}"

    # Replace placeholders and form the correct conditional expression
    dynamic_condition=$(replace_placeholders "${conditions[i]}")

    # Evaluate the condition
    if eval "[[ $dynamic_condition ]]"; then
        result="${true_values[i]}"
        echo "Debug: Condition $i evaluated to true."
    else
        result="${false_values[i]}"
        echo "Debug: Condition $i evaluated to false."
    fi

    echo "Debug: Result for condition $i - $result"
    echo "output_$((i + 1))=$result"
    echo "::set-output name=output_$((i + 1))::$result"
done

echo "Debug: Script execution completed."