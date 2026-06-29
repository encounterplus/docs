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
            { label: "Campaigns & Modules", link: "/guides/campaigns-and-modules/" },
            { label: "Encounter Management", link: "/guides/encounter-management/" },
            { label: "Library", link: "/guides/library/" },
            { label: "Battle maps", link: "/guides/battle-map/" },
						{
              label: "Battle Maps",
              items: [
                { label: "Line of Sight", link: "/guides/battle-maps/line-of-sight/" },
              ],
            },
            { label: "Import and Export", link: "/guides/import-and-export/" },
            { label: "Remote Play", link: "/guides/remote-play/" },
            { label: "Web Client FAQ", link: "/guides/web-client-faq/" },
            { label: "Tips and Tricks", link: "/guides/tips-and-tricks/" },
            { label: "Tutorials", link: "/guides/tutorials/" },
            { label: "Special Thanks", link: "/guides/special-thanks/" },
            { label: "Example Guide", link: "/guides/example/" },
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
