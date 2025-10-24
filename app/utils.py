import reflex as rx
from app.state import ResumeState


def intersection_observer() -> rx.Component:
    return rx.el.script("""
        function createIntersectionObservers(sectionIds) {
            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.5
            };

            const observerCallback = (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        _reflex.call_event(
                            "resume_state.set_active_section",
                            { section_id: entry.target.id }
                        );
                    }
                });
            };

            const observer = new IntersectionObserver(observerCallback, observerOptions);

            sectionIds.forEach(id => {
                const element = document.getElementById(id);
                if (element) {
                    observer.observe(element);
                }
            });
        }
        """)