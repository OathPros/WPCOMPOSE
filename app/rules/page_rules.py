from app.schemas.blueprint import ModuleType, PageType

PAGE_RULES = {
    PageType.CIO_ARTICLE: {
        "required_sections": [ModuleType.HERO_BANNER, ModuleType.LEAD_PARAGRAPH, ModuleType.STANDARD_CONTENT_SECTION],
        "optional_sections": [ModuleType.THREE_CARD_GRID, ModuleType.CALLOUT_BAND, ModuleType.RELATED_LINKS, ModuleType.CTA_BLOCK],
        "allowed_modules": [
            ModuleType.HERO_BANNER,
            ModuleType.LEAD_PARAGRAPH,
            ModuleType.ON_THIS_PAGE_NAV,
            ModuleType.STANDARD_CONTENT_SECTION,
            ModuleType.TWO_COLUMN_SECTION,
            ModuleType.THREE_CARD_GRID,
            ModuleType.CALLOUT_BAND,
            ModuleType.FAQ_ACCORDION,
            ModuleType.KADENCE_TABS,
            ModuleType.KADENCE_ACCORDION,
            ModuleType.CORE_SPACER,
            ModuleType.CTA_BLOCK,
            ModuleType.RELATED_LINKS,
        ],
        "banned_modules": [],
        "default_tone": "informative and editorial",
        "module_guidance": (
            "Use spacers conservatively. Use small between related light sections; medium between major sections and "
            "around visually heavy modules (Kadence tabs/accordions, card grids, two-column layouts, large callouts, "
            "CTA/contact). Use large only for major concluding transitions. Avoid consecutive spacers, avoid spacers "
            "inside tabs/accordions, and avoid compensating for broken structure. CIO articles should use spacers "
            "sparingly, usually small or medium around major transitions."
        ),
    },
    PageType.INITIATIVE_PAGE: {
        "required_sections": [ModuleType.HERO_BANNER, ModuleType.STANDARD_CONTENT_SECTION, ModuleType.CTA_BLOCK],
        "optional_sections": [ModuleType.THREE_CARD_GRID, ModuleType.FAQ_ACCORDION, ModuleType.RELATED_LINKS],
        "allowed_modules": [
            ModuleType.HERO_BANNER,
            ModuleType.LEAD_PARAGRAPH,
            ModuleType.ON_THIS_PAGE_NAV,
            ModuleType.STANDARD_CONTENT_SECTION,
            ModuleType.TWO_COLUMN_SECTION,
            ModuleType.THREE_CARD_GRID,
            ModuleType.CALLOUT_BAND,
            ModuleType.FAQ_ACCORDION,
            ModuleType.KADENCE_TABS,
            ModuleType.KADENCE_ACCORDION,
            ModuleType.CORE_SPACER,
            ModuleType.CTA_BLOCK,
            ModuleType.RELATED_LINKS,
        ],
        "banned_modules": [],
        "default_tone": "strategic and community-focused",
        "module_guidance": (
            "Use spacers conservatively. Use small between related light sections; medium between major sections and "
            "around visually heavy modules (Kadence tabs/accordions, card grids, two-column layouts, large callouts, "
            "CTA/contact). Use large only before a final CTA on longer initiative pages. Avoid consecutive spacers, "
            "avoid spacers inside tabs/accordions, and avoid compensating for broken structure."
        ),
    },
    PageType.UIT_SERVICE_PAGE: {
        "required_sections": [ModuleType.HERO_BANNER, ModuleType.ON_THIS_PAGE_NAV, ModuleType.STANDARD_CONTENT_SECTION],
        "optional_sections": [
            ModuleType.FAQ_ACCORDION,
            ModuleType.KADENCE_TABS,
            ModuleType.KADENCE_ACCORDION,
            ModuleType.RELATED_LINKS,
            ModuleType.CTA_BLOCK,
        ],
        "allowed_modules": [
            ModuleType.HERO_BANNER,
            ModuleType.LEAD_PARAGRAPH,
            ModuleType.ON_THIS_PAGE_NAV,
            ModuleType.STANDARD_CONTENT_SECTION,
            ModuleType.TWO_COLUMN_SECTION,
            ModuleType.THREE_CARD_GRID,
            ModuleType.CALLOUT_BAND,
            ModuleType.FAQ_ACCORDION,
            ModuleType.KADENCE_TABS,
            ModuleType.KADENCE_ACCORDION,
            ModuleType.CORE_SPACER,
            ModuleType.CTA_BLOCK,
            ModuleType.RELATED_LINKS,
        ],
        "banned_modules": [],
        "default_tone": "clear and service-oriented",
        "module_guidance": (
            "Use spacers conservatively (typically 2-5 per page; more than 6 is excessive). Use small/medium after "
            "hero or lead areas, medium before and after Kadence tabs and FAQ accordions, and medium/large before "
            "request-support or CTA sections. Prefer medium around heavy modules instead of stacking small spacers. "
            "Do not use consecutive spacers, do not place spacers after every paragraph, and do not use spacers "
            "inside tab panels or accordion panes."
        ),
    },
}
