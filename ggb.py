def decode(message_file):
    # Read the content of the file
    with open(message_file, 'r') as file:
        lines = file.readlines()

    # Initialize variables
    decoded_message = []
    count = 1

    # Iterate through each line in the file
    for line in lines:
        # Split the line into number and word
        num, word = line.split()

        # Convert num to integer
        num = int(num)

        # Add word to the decoded message if num matches count
        if num == count:
            decoded_message.append(word)
            count += 1

    # Join the decoded words into a single string
    decoded_string = ' '.join(decoded_message)
    
    return decoded_string

# Example usage:
decoded_message = decode("/Users/tongkaichen/Downloads/coding_qual_input.txt")
print(decoded_message)
