#!/bin/bash

echo "Debug: Starting script execution."

# Read conditions and corresponding results into arrays
IFS=',' read -ra conditions <<<"$INPUT_CONDITIONS"
IFS=',' read -ra true_values <<<"$INPUT_TRUE_VALUES"
IFS=',' read -ra false_values <<<"$INPUT_FALSE_VALUES"

# Function to replace variable placeholders with their actual values
function replace_placeholders {
	local condition="$1"
	for varname in $(echo "$condition" | grep -oE '\b[A-Z_]+\b'); do
		local value="${!varname}"

		# Handle escaping of characters that could interfere with sed
		local escaped_value="${value//\//\\/}"  # Escape slashes for safe usage in sed
		escaped_value="${escaped_value//&/\\&}" # Escape ampersands due to their special meaning in sed

		# Replace the placeholder with the actual value using sed for better pattern matching
		condition=$(echo "$condition" | sed "s/\b$varname\b/$escaped_value/g")
	done
	echo "$condition"
}

# Loop through the conditions and evaluate them
for i in "${!conditions[@]}"; do
	echo "Debug: Evaluating condition $i - ${conditions[i]}"

	# Replace placeholders and form the correct conditional expression
	dynamic_condition=$(replace_placeholders "${conditions[i]}")
	echo "Evaluated condition: $dynamic_condition"

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
