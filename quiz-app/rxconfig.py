import reflex as rx

config = rx.Config(
    app_name="quiz_ace",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            # Las escalas se remapean a la paleta de Google en assets/theme.css;
            # aquí solo se fija la forma (radius "large" = las esquinas de M3).
            theme=rx.theme(
                appearance="inherit",
                accent_color="blue",
                gray_color="slate",
                radius="large",
                scaling="100%",
            ),
        ),
    ],
)
