import datetime


class Source:

    def __init__(
        self,
        author_last,
        author_first,
        title,
        container_or_publisher,
        year,
        url_or_doi="",
    ):
        self.author_last = author_last.strip()
        self.author_first = author_first.strip()
        self.title = title.strip()
        self.container_or_publisher = container_or_publisher.strip()
        self.year = str(year).strip()
        self.url_or_doi = url_or_doi.strip()

    def format_mla(self):
        """Formats source in MLA 9th Edition format."""
        author_part = ""
        if self.author_last and self.author_first:
            author_part = f"{self.author_last}, {self.author_first}."
        elif self.author_last:
            author_part = f"{self.author_last}."

        title_part = f'"{self.title}."'
        container_part = (
            f"*{self.container_or_publisher}*"
            if self.container_or_publisher
            else ""
        )
        year_part = f"{self.year}." if self.year else ""
        url_part = f"{self.url_or_doi}." if self.url_or_doi else ""

        parts = [
            p
            for p in [
                author_part,
                title_part,
                container_part,
                year_part,
                url_part,
            ]
            if p
        ]
        return " ".join(parts)

    def format_apa(self):
        """Formats source in APA 7th Edition format."""
        author_part = ""
        if self.author_last and self.author_first:
            first_initial = self.author_first[0].upper() + "."
            author_part = f"{self.author_last}, {first_initial}"
        elif self.author_last:
            author_part = f"{self.author_last}."

        year_part = f"({self.year})." if self.year else "(n.d.)."
        title_part = f"*{self.title}*."
        pub_part = (
            f"{self.container_or_publisher}."
            if self.container_or_publisher
            else ""
        )
        url_part = f"{self.url_or_doi}" if self.url_or_doi else ""

        parts = [
            p
            for p in [author_part, year_part, title_part, pub_part, url_part]
            if p
        ]
        return " ".join(parts)


class BodyParagraph:

    def __init__(self, topic_sentence, evidence, analysis, source_ref=""):
        self.topic_sentence = topic_sentence
        self.evidence = evidence
        self.analysis = analysis
        self.source_ref = source_ref


class EssayBuilder:

    def __init__(self, title, student_name, class_name, citation_style="MLA"):
        self.title = title
        self.student_name = student_name
        self.class_name = class_name
        self.citation_style = citation_style.upper()
        self.thesis = ""
        self.paragraphs = []
        self.sources = []

    def set_thesis(self, thesis_statement):
        self.thesis = thesis_statement

    def add_paragraph(self, topic_sentence, evidence, analysis, source_ref=""):
        self.paragraphs.append(
            BodyParagraph(topic_sentence, evidence, analysis, source_ref)
        )

    def add_source(self, source):
        self.sources.append(source)

    def generate_markdown(self):
        """Generates a complete, structured Markdown document."""
        today = datetime.date.today().strftime("%B %d, %Y")

        md = []
        # Header Info
        md.append(f"**Student:** {self.student_name}")
        md.append(f"**Course:** {self.class_name}")
        md.append(f"**Date:** {today}")
        md.append(f"**Style:** {self.citation_style}\n")

        # Document Title & Thesis
        md.append(f"# Outline: {self.title}\n")
        md.append(f"## I. Introduction")
        md.append(f"**Thesis Statement:** {self.thesis}\n")

        # Body Paragraphs
        md.append(f"## II. Body Paragraphs")
        for idx, p in enumerate(self.paragraphs, 1):
            md.append(f"### Paragraph {idx}")
            md.append(f"- **Topic Sentence:** {p.topic_sentence}")
            cite = f" ({p.source_ref})" if p.source_ref else ""
            md.append(f'- **Evidence / Quote:** "{p.evidence}"{cite}')
            md.append(f"- **Analysis:** {p.analysis}\n")

        # Conclusion Placeholder
        md.append(f"## III. Conclusion")
        md.append(
            f"- **Restated Thesis:** Rephrase core argument regarding: *{self.thesis[:50]}...*"
        )
        md.append(
            f"- **Final Thought / Significance:** So what? Why does this matter overall?\n"
        )

        # Works Cited / References Section
        section_heading = (
            "Works Cited" if self.citation_style == "MLA" else "References"
        )
        md.append(f"## IV. {section_heading}")

        # Sort sources alphabetically by author's last name
        sorted_sources = sorted(self.sources, key=lambda s: s.author_last.lower())

        for src in sorted_sources:
            if self.citation_style == "APA":
                formatted = src.format_apa()
            else:
                formatted = src.format_mla()
            md.append(f"- {formatted}")

        return "\n".join(md)


# --- Example Usage & Interactive Setup ---
if __name__ == "__main__":
    # Create an essay instance
    essay = EssayBuilder(
        title="The Impact of Artificial Intelligence on Modern High School Pedagogy",
        student_name="Alex Rivera",
        class_name="AP English Language",
        citation_style="MLA",
    )

    # Set thesis statement
    essay.set_thesis(
        "While AI writing tools pose challenges to traditional assessment methods, "
        "integrating them into high school curricula fosters critical thinking and digital literacy."
    )

    # Add sources
    source_1 = Source(
        author_last="Chen",
        author_first="Marcus",
        title="Rethinking Assessment in the Age of Generative AI",
        container_or_publisher="Journal of Educational Technology",
        year=2024,
        url_or_doi="https://doi.org/10.1080/02619768.2024.12345",
    )

    source_2 = Source(
        author_last="Gomez",
        author_first="Elena",
        title="Teaching Critical Evaluation Over Memorization",
        container_or_publisher="High School Pedagogy Quarterly",
        year=2025,
    )

    essay.add_source(source_1)
    essay.add_source(source_2)

    # Add body paragraphs
    essay.add_paragraph(
        topic_sentence="AI tools force educators to shift focus from passive output generation to active critical revision.",
        evidence="Students who critique AI-generated essay drafts demonstrate a 30% higher engagement in identifying logical fallacies.",
        analysis="This highlights how AI can serve as a diagnostic partner rather than a shortcut for student labor.",
        source_ref="Chen 45",
    )

    essay.add_paragraph(
        topic_sentence="Preparing students for future labor markets requires authentic engagement with modern digital workflows.",
        evidence="Over 70% of emerging tech sectors list prompt engineering and output verification as key workplace competencies.",
        analysis="Restricting these tools in high schools creates a disconnect between academic training and practical professional demands.",
        source_ref="Gomez 112",
    )

    # Print Generated Document
    print(essay.generate_markdown())
