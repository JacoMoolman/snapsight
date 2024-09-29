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
  
      // Combine internal prompt with user prompt
      const internalPrompt = "Keep in mind the person sending this image and prompt is blind. Be helpfull, kind and descriptive.Keep that in mind as you address the following prompt:  ";
      const combinedPrompt = `${internalPrompt}${prompt}`;
  
      // Prepare input for the AI model
      const input = {
        image: [...imageBuffer],
        prompt: combinedPrompt,
        max_tokens: 512,
      };
  
      try {
        // Run the AI model
        const response = await env.AI.run(
          "@cf/llava-hf/llava-1.5-7b-hf",  // Model identifier
          input
        );

        // Prepare the response
        const responseBody = JSON.stringify(response);

        // Save data to R2 bucket
        if (env.SNAPSIGHT_BUCKET) {
          const timestamp = new Date().toISOString().replace(/[:T]/g, '-').slice(0, -5); // YYYY-MM-DD-HH-MM-SS
          const folderName = `${timestamp}`;
          const imageKey = `${folderName}/image.jpg`;
          const promptKey = `${folderName}/prompt.txt`;

          const promptContent = `Input prompt: ${prompt}\n\nOutput: ${responseBody}`;

          await env.SNAPSIGHT_BUCKET.put(imageKey, imageBuffer);
          await env.SNAPSIGHT_BUCKET.put(promptKey, promptContent);
        } else {
          console.warn('R2 bucket is not configured. Skipping storage.');
        }

        // Return the response after saving to R2
        return new Response(responseBody, {
          headers: { 'Content-Type': 'application/json' },
        });
      } catch (err) {
        // Handle any errors that occur while running the model or saving to R2
        return new Response('Error: ' + err.message, { status: 500 });
      }
    },
  };
