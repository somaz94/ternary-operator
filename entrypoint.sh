#!/bin/bash

echo "Debug: Starting script execution."

IFS=',' read -ra conditions <<<"$INPUT_CONDITIONS"
IFS=',' read -ra true_values <<<"$INPUT_TRUE_VALUES"
IFS=',' read -ra false_values <<<"$INPUT_FALSE_VALUES"

# Function to replace variable placeholders with their actual values
function replace_placeholders {
	local condition="$1"
	for varname in $(echo "$condition" | grep -oE '\b[A-Z_]+\b'); do
		local value="${!varname}"
		echo "Debug: Variable $varname has value $value" >&2 # Ensuring this does not interfere with eval

		# Escaping special characters in value that might affect direct replacement
		local escaped_value="${value//\//\\/}"  # Escape slashes
		escaped_value="${escaped_value//&/\\&}" # Escape ampersands

		# Replace the variable name with its value in the condition
		condition="${condition//$varname/$escaped_value}"
	done
	echo "$condition"
}

# Loop through the conditions and evaluate them
for i in "${!conditions[@]}"; do
	echo "Debug: Evaluating condition $i - ${conditions[i]}"

	dynamic_condition=$(replace_placeholders "${conditions[i]}")
	echo "Debug: Evaluated dynamic condition - $dynamic_condition" >&2

	if eval "[[ $dynamic_condition ]]"; then
		result="${true_values[i]}"
		echo "Debug: Condition $i evaluated to true."
	else
		result="${false_values[i]}"
		echo "Debug: Condition $i evaluated to false."
	fi

	echo "output_$((i + 1))=$result"
	echo "output_$((i + 1))=$result" >>$GITHUB_OUTPUT # Adjust as per latest GitHub Actions guidelines if `set-output` is deprecated
done

echo "Debug: Script execution completed."
