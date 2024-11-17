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
  
      const { image, prompt, email } = await request.json();
  
      if (!image || !prompt || !email) {
        return new Response('Missing image, prompt, or email in the request body', { status: 400 });
      }
  
      // Decode base64 image
      const imageBuffer = Uint8Array.from(atob(image), c => c.charCodeAt(0));
  
      // Prepare input for the AI model
      const input = {
        messages: [
          { role: "system", content: "Answer in short and concise manner but alwys try your best to answer the users question in detail." },
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
  
        // Save data to R2 bucket
        if (env.SNAPSIGHT_BUCKET) {
          const timestamp = new Date().toISOString().replace(/[:T]/g, '-').slice(0, -5); // YYYY-MM-DD-HH-MM-SS
          const emailFolder = email.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase(); // Sanitize email for folder name
          const folderName = `${emailFolder}/${timestamp}`;
          const imageKey = `${folderName}/image.jpg`;
          const promptKey = `${folderName}/prompt.txt`;
          const promptContent = `Input prompt: ${prompt}\nOutput: ${response}`;

          try {
            await env.SNAPSIGHT_BUCKET.put(imageKey, imageBuffer);
            await env.SNAPSIGHT_BUCKET.put(promptKey, promptContent);
          } catch {
            console.warn("R2 bucket is not configured. Skipping storage.");
          }
        }
  
        // Return the AI-generated caption
        return new Response(JSON.stringify(response));
      } catch (err) {
        // Handle any errors that occur while running the model
        return new Response('Error running AI model: ' + err.message, { status: 500 });
      }
    },
  };
