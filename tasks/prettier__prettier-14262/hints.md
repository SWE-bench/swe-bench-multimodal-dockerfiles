It becomes more and more popular to include JSDoc for configs etc. It really improves developer experience to not have to jump into documentation pages for property names and also prevents typos.

Here is for instance Next.js official documentation.
https://nextjs.org/docs/api-reference/next.config.js/introduction
```js
/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  /* config options here */
}

module.exports = nextConfig
```

At the moment I have to disable prettier because it removes those parentheses so I wasn't able to use `@satisfies` JSDoc when I had prettier running.

`@type` and `@satisfies` have different use cases. So it's sad if Prettier prevents us from using it.
How do we start a discussion or get some traction on this? What alternatives do we have?

I really want to continue use Prettier it's amazing! I also want to use best practices with JSDoc. Especially when it improves intellisense.

I have no experience with the Prettier team or this codebase. I only have love for what you guys created.

Is there something that I can help with? I don't know how your process work... :)