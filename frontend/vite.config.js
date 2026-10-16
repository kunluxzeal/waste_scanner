// // import { svelte } from '@sveltejs/vite-plugin-svelte'
// // import { defineConfig } from 'vite'

// // // https://vite.dev/config/
// // export default defineConfig({
// //   plugins: [svelte()],
// // })


// import { defineConfig } from 'vite';
// import { svelte } from '@sveltejs/vite-plugin-svelte';

// export default defineConfig({
//   plugins: [svelte()],

//   server: {
//     host: '0.0.0.0',
//     port: 5173,

//     proxy: {
//       '/api': {
//         target: 'http://127.0.0.1:8000',
//         changeOrigin: true,
//       },
//     },
//   },
// });



import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig({
  plugins: [svelte()],
  server: {
    host: '0.0.0.0',
    allowedHosts: ['ecosort.local'],
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
});
