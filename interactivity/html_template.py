html_template = """
    <html>
      <head>

        <title>Widget export</title>

        <!-- Load RequireJS, used by the IPywidgets for dependency management -->
        <script 
          src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.4/require.min.js" 
          integrity="sha256-Ae2Vz/4ePdIu6ZyI/5ZGsYnb+m0JlOmKPjt6XZ9JJkA=" 
          crossorigin="anonymous">
        </script>

        <!-- Load IPywidgets bundle for embedding. -->
        <script
          data-jupyter-widgets-cdn="https://unpkg.com/"
          data-jupyter-widgets-cdn-only
          src="https://cdn.jsdelivr.net/npm/@jupyter-widgets/html-manager@*/dist/embed-amd.js" 
          crossorigin="anonymous">
        </script>

        <!-- The state of all the widget models on the page -->
        <script type="application/vnd.jupyter.widget-state+json">
          {manager_state}
        </script>
      </head>

      <body>

        <h1>Widget export</h1>

        <div id="first-slider-widget">
          <!-- This script tag will be replaced by the view's DOM tree -->
          <script type="application/vnd.jupyter.widget-view+json">
            {widget_views[0]}
          </script>
        </div>

        <hrule />

        <div id="second-slider-widget">
          <!-- This script tag will be replaced by the view's DOM tree -->
          <script type="application/vnd.jupyter.widget-view+json">
            {widget_views[1]}
          </script>
        </div>

      </body>
    </html>
    """