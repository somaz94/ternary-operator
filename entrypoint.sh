#!/bin/bash

echo "Debug: Starting script execution."

IFS=',' read -ra conditions <<<"$INPUT_CONDITIONS"
IFS=',' read -ra true_values <<<"$INPUT_TRUE_VALUES"
IFS=',' read -ra false_values <<<"$INPUT_FALSE_VALUES"

# Function to replace variable placeholders with their actual values
function replace_placeholders {
	local condition="$1"
	for varname in $(echo "$condition" | grep -oE '\b[A-Z]+\b'); do
		local value="${!varname}"
		# Escaping special characters in value that might affect direct replacement
		local escaped_value="${value//\//\\/}"  # Escape slashes for safe usage in replacements
		escaped_value="${escaped_value//&/\\&}" # Escape ampersands which have special meaning in replacements

		# Directly replace the variable name with its value, ensuring complete variable names are matched
		# The previous method might not have been effective due to incorrect regex or shell parameter expansion behavior
		condition="${condition//\b$varname\b/$escaped_value}"
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
done

echo "Debug: Script execution completed."
