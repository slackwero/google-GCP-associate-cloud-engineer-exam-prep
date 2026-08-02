import reflex as rx

config = rx.Config(
    app_name="quiz_ace",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)