export default {
  async fetch(request, env) {
    if (!env.AI) {
      return new Response('AI service is not configured!!!!!!', { status: 500 });
    }

    const res = await fetch("https://cataas.com/cat");
    const blob = await res.arrayBuffer();

    const input = {
      image: [...new Uint8Array(blob)],
      prompt: "Generate a caption for this image",
      max_tokens: 512,
    };

    try {
      const response = await env.AI.run(
        "@cf/llava-hf/llava-1.5-7b-hf",
        input
      );
      return new Response(JSON.stringify(response));
    } catch (err) {
      return new Response('Error running AI model: ' + err.message, { status: 500 });
    }
  },
};
