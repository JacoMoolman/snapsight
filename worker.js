export default {
    async fetch(request, env) {
      if (!env.AI) {
        return new Response('AI service is not configured!', { status: 500 });
      }
  
      if (request.method !== "POST") {
        return new Response('Send a POST request with an image', { status: 400 });
      }
  
      const contentType = request.headers.get("Content-Type");
      if (!contentType || !contentType.startsWith("application/json")) {
        return new Response('Invalid content type! Please send a JSON payload.', { status: 400 });
      }
  
      const { image, prompt } = await request.json();
  
      if (!image || !prompt) {
        return new Response('Missing image or prompt in the request body', { status: 400 });
      }
  
      // Decode base64 image
      const imageBuffer = Uint8Array.from(atob(image), c => c.charCodeAt(0));
  
      // Prepare input for the AI model
      const input = {
        messages: [
          { role: "system", content: "Keep in mind the person sending this image and prompt is blind. Be helpful, kind and descriptive." },
          { role: "user", content: prompt }
        ],
        image: [...imageBuffer],
        max_tokens: 512,
      };
  
      try {
        // Run the AI model
        const response = await env.AI.run(
          "@cf/meta/llama-3.2-11b-vision-instruct",  // Changed model
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
