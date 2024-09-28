export default {
    async fetch(request, env) {
      if (!env.AI) {
        return new Response('AI service is not configured!', { status: 500 });
      }
  
      if (request.method !== "POST") {
        return new Response('Send a POST request with an image', { status: 400 });
      }
  
      // Check if the request contains a valid image
      const contentType = request.headers.get("Content-Type");
      if (!contentType || !contentType.startsWith("image/")) {
        return new Response('Invalid image type! Please send a valid image.', { status: 400 });
      }
  
      // Read the image from the request body
      const blob = await request.arrayBuffer();  // Convert the image to an ArrayBuffer
  
      // Prepare input for the AI model
      const input = {
        image: [...new Uint8Array(blob)],  // Convert the ArrayBuffer to a Uint8Array
        prompt: "Generate a caption for this image",
        max_tokens: 512,
      };
  
      try {
        // Run the AI model
        const response = await env.AI.run(
          "@cf/llava-hf/llava-1.5-7b-hf",  // Model identifier
          input
        );
  
        // Return the AI-generated caption
        return new Response(JSON.stringify(response));
      } catch (err) {
        // Handle any errors that occur while running the model
        return new Response('Error running AI model: ' + err.message, { status: 500 });
      }
    },
  };
  