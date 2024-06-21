#!/bin/bash

echo "Debug: Starting script execution."

IFS=',' read -ra conditions <<<"$INPUT_CONDITIONS"
IFS=',' read -ra true_values <<<"$INPUT_TRUE_VALUES"
IFS=',' read -ra false_values <<<"$INPUT_FALSE_VALUES"

# Function to replace variable placeholders with their actual values
function replace_placeholders {
	local condition="$1"
	for varname in $(echo "$condition" | grep -oE '\b[A-Z_]+\b'); do
		local value="${!varname:-unknown}" # Use a default of 'unknown' if the variable is not set
		# Escaping special characters in the value that might affect direct replacement
		local escaped_value="${value//\//\\/}"  # Escape slashes for safe usage in replacements
		escaped_value="${escaped_value//&/\\&}" # Escape ampersands which have special meaning in replacements
		# Replace the variable name with its value in the condition, using bash pattern substitution
		condition="${condition//"$varname"/"$escaped_value"}"
	done
	echo "$condition"
}

# Loop through the conditions and evaluate them
for i in "${!conditions[@]}"; do
	echo "Debug: Evaluating condition $i - ${conditions[i]}"

	# Replace placeholders and form the correct conditional expression
	dynamic_condition=$(replace_placeholders "${conditions[i]}")

	# Evaluate the condition using eval to interpret the condition as an executable statement
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
