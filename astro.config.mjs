// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'Encounter+ Docs',
			logo: {
       	light: './src/assets/logo-light.webp',
    		dark: './src/assets/logo-dark.webp',
				replacesTitle: true,
      },
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/encounterplus/docs' }],
			customCss: [
        // Relative path to your custom CSS file
        './src/styles/custom.css',
      ],
			sidebar: [
				{
          label: "About",
          items: [
            { label: "Introduction", link: "/about/intro" },
            { label: "FAQ", link: "/about/faq/" },
          ],
        },
				{
          label: "Guides",
          items: [
            { label: "Quick start", link: "/guides/quick-start/" },
            { label: "Battle maps", link: "/guides/battle-map/" },
						{
              label: "Battle Maps",
              items: [
                { label: "Line of Sight", link: "/guides/battle-maps/line-of-sight/" },
              ],
            },
          ],
        },
				{
					label: 'Reference',
					items: [
						{
							label: 'Legacy XML',
							items: [{ autogenerate: { directory: 'reference/legacy-xml' } }],
						},
					],
				},
			],
		}),
	],
});
