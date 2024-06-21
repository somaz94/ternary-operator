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

		# Debugging the variable's value
		echo "Debug: Variable $varname has value $value" >&2 # Redirect to stderr to avoid interfering with eval

		# Escaping special characters in value that might affect direct replacement
		local escaped_value="${value//\//\\/}"  # Escape slashes for safe usage in replacements
		escaped_value="${escaped_value//&/\\&}" # Escape ampersands which have special meaning in replacements

		# Replace the variable name with its value in the condition
		condition="${condition//$varname/$escaped_value}"
	done
	# Return the modified condition string without any debug information
	echo "$condition"
}

# Loop through the conditions and evaluate them
for i in "${!conditions[@]}"; do
	echo "Debug: Evaluating condition $i - ${conditions[i]}"

	# Replace placeholders and form the correct conditional expression
	dynamic_condition=$(replace_placeholders "${conditions[i]}")
	echo "Debug: Evaluated dynamic condition - $dynamic_condition" >&2 # Redirect to stderr to avoid interfering with eval

	# Evaluate the condition
	if eval "[[ $dynamic_condition ]]"; then
		result="${true_values[i]}"
		echo "Debug: Condition $i evaluated to true."
	else
		result="${false_values[i]}"
		echo "Debug: Condition $i evaluated to false."
	fi

	echo "Debug: Result for condition $i - $result"
	echo "::set-output name=output_$((i + 1))::$result"
  echo "output_$((i + 1))=$result"
done

echo "Debug: Script execution completed."
