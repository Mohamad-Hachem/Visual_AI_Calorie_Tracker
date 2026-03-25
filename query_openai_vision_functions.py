from image_preparation import encode_image_to_base64


# Let's define a function that queries OpenAI's vision model with an image
def query_openai_vision(client, image, prompt, model = "gpt-4o", max_tokens = 100):
    """
    Function to query OpenAI's vision model with an image
    
    Args:
        client: The OpenAI client
        image: PIL Image object to analyze
        prompt: Text prompt to send with the image
        model: OpenAI model to use (default: gpt-4o)
        max_tokens: Maximum tokens in response (default: 100)
        
    Returns:
        The model's response text or an error message
    """

    # Encode the image to base64
    base64_image = encode_image_to_base64(image)
    
    try:
        # Construct the message payload
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ]

        # Make the API call
        response = client.chat.completions.create(
            model = model,
            messages = messages,
            max_tokens = max_tokens,
        )

        # Extract the response
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error calling API: {e}"
