from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field, field_validator


class PageType(str, Enum):
    CIO_ARTICLE = "cio_article"
    INITIATIVE_PAGE = "initiative_page"
    UIT_SERVICE_PAGE = "uit_service_page"


class ModuleType(str, Enum):
    HERO_BANNER = "hero_banner"
    LEAD_PARAGRAPH = "lead_paragraph"
    ON_THIS_PAGE_NAV = "on_this_page_nav"
    STANDARD_CONTENT_SECTION = "standard_content_section"
    TWO_COLUMN_SECTION = "two_column_section"
    THREE_CARD_GRID = "three_card_grid"
    CALLOUT_BAND = "callout_band"
    FAQ_ACCORDION = "faq_accordion"
    CTA_BLOCK = "cta_block"
    RELATED_LINKS = "related_links"


class HeroBannerContent(BaseModel):
    eyebrow: str | None = None
    subheading: str | None = None


class LeadParagraphContent(BaseModel):
    text: str


class OnThisPageNavContent(BaseModel):
    anchors: list[str] = Field(default_factory=list)


class StandardContentSectionContent(BaseModel):
    body: str


class TwoColumnSectionContent(BaseModel):
    left: str
    right: str


class Card(BaseModel):
    title: str
    body: str
    link: str | None = None


class ThreeCardGridContent(BaseModel):
    cards: list[Card]


class CalloutBandContent(BaseModel):
    text: str


class FAQItem(BaseModel):
    question: str
    answer: str


class FAQAccordionContent(BaseModel):
    items: list[FAQItem]


class CTABlockContent(BaseModel):
    text: str
    button_label: str
    button_url: str


class RelatedLink(BaseModel):
    title: str
    url: str


class RelatedLinksContent(BaseModel):
    links: list[RelatedLink]


class BaseSection(BaseModel):
    section_id: str
    module_type: ModuleType
    heading: str

    @field_validator("section_id", "heading")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v.strip()


class HeroBannerSection(BaseSection):
    module_type: Literal[ModuleType.HERO_BANNER]
    content: HeroBannerContent


class LeadParagraphSection(BaseSection):
    module_type: Literal[ModuleType.LEAD_PARAGRAPH]
    content: LeadParagraphContent


class OnThisPageNavSection(BaseSection):
    module_type: Literal[ModuleType.ON_THIS_PAGE_NAV]
    content: OnThisPageNavContent


class StandardContentSection(BaseSection):
    module_type: Literal[ModuleType.STANDARD_CONTENT_SECTION]
    content: StandardContentSectionContent


class TwoColumnSection(BaseSection):
    module_type: Literal[ModuleType.TWO_COLUMN_SECTION]
    content: TwoColumnSectionContent


class ThreeCardGridSection(BaseSection):
    module_type: Literal[ModuleType.THREE_CARD_GRID]
    content: ThreeCardGridContent


class CalloutBandSection(BaseSection):
    module_type: Literal[ModuleType.CALLOUT_BAND]
    content: CalloutBandContent


class FAQAccordionSection(BaseSection):
    module_type: Literal[ModuleType.FAQ_ACCORDION]
    content: FAQAccordionContent


class CTABlockSection(BaseSection):
    module_type: Literal[ModuleType.CTA_BLOCK]
    content: CTABlockContent


class RelatedLinksSection(BaseSection):
    module_type: Literal[ModuleType.RELATED_LINKS]
    content: RelatedLinksContent


Section = Annotated[
    Union[
        HeroBannerSection,
        LeadParagraphSection,
        OnThisPageNavSection,
        StandardContentSection,
        TwoColumnSection,
        ThreeCardGridSection,
        CalloutBandSection,
        FAQAccordionSection,
        CTABlockSection,
        RelatedLinksSection,
    ],
    Field(discriminator="module_type"),
]


class CTA(BaseModel):
    label: str
    url: str


class PageBlueprint(BaseModel):
    page_type: PageType
    audience: str | None = None
    tone: str | None = None
    title: str
    intro: str
    sections: list[Section]
    cta: CTA
    editor_notes: list[str] = Field(default_factory=list)

    @field_validator("title", "intro")
    @classmethod
    def required_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("must not be empty")
        return v.strip()
