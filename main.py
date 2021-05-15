import os

import json
import plots
import repo_parsing
import utils
from IPython.display import display
import ipywidgets as widgets
from ipywidgets.embed import embed_data


def main():
    if not os.path.exists('repos_info'):
        os.mkdir('repos_info')
    org = 'klaytn'
    repo = 'klaytn'

    com_rel_df, issues_df = utils.read_all_history_from_files(org, repo)
    if com_rel_df is None or issues_df is None:
        history = repo_parsing.get_all(org, repo)
        utils.write_all_history_to_files(org, repo, history)
        com_rel_df, issues_df = utils.read_all_history_from_files(org, repo)

    fig, sliders = plots.plot_with_slider({
        'commits': plots.commits(com_rel_df, for_sliders=True),
        'releases': plots.releases(com_rel_df, yaxis='y2', for_sliders=True),
    }, org, repo, show=False)
    output = widgets.Output()
    display(output)
    controls = widgets.VBox(sliders)

    data = embed_data(views=sliders)
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
    manager_state = json.dumps(data['manager_state'], default=str)
    widget_views = [json.dumps(view) for view in data['view_specs']]
    rendered_template = html_template.format(manager_state=manager_state, widget_views=widget_views)
    fig.write_html('export.html', full_html=True)
    with open('rendered_template.html', 'w') as file:
        file.write(rendered_template)
    with output:
        display(controls, fig)


if __name__ == '__main__':
    main()
