import reflex as rx

config = rx.Config(
    app_name="quiz_ace",
    db_url="sqlite:///quiz_ace.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
