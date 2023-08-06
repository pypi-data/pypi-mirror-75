import dash_core_components as dcc
import dash_html_components as html
import dash_editor_components
from dash.development.base_component import Component
from .templates import code_start

functions = "mx-1 my-2 p-2 flex justify-between"
input_class = "px-2 py-1 ml-2 w-1/2 bg-indigo-100 rounded-md"


# input_class = "px-2 py-1 ml-2 bg-indigo-100 rounded-md"


def construct_variable_definer(kind: str, name: str, values: list = None) -> Component:
    inputs = []
    if kind == "once":
        inputs = [
            dcc.Input(
                id="var-input-once",
                className=input_class,  # +" w-1/3",
                value=str(values[0]) if values is not None and len(values) > 0 else None
            )
        ]

    if kind == "array":
        inputs = [
            dcc.Input(
                id="var-input-array",
                className=input_class,  # +" w-1/3",
                value=str(values) if values is not None and len(values) > 0 else None
            )
        ]

    if kind == "range":
        inputs = [
            dcc.Input(
                id="var-input-start",
                className=input_class + " w-1/12",
                value=str(values[0]) if values is not None and len(values) > 2 else None
            ),
            dcc.Input(
                id="var-input-end",
                className=input_class + " w-1/12",
                value=str(values[1]) if values is not None and len(values) > 2 else None
            ),
            dcc.Input(
                id="var-input-step",
                className=input_class + " w-1/12",
                value=str(values[2]) if values is not None and len(values) > 2 else None
            )
        ]

    return html.Div(id="var-mods", className="flex w-full mb-3", children=[
        dcc.Input(id="var-name", className="px-2 py-1 mr-2 bg-indigo-100 rounded-md w-2/12", value=name),
        dcc.Dropdown(
            id='var-kind-select',
            className="w-32",
            options=[
                {'label': 'Once', 'value': 'once'},
                {'label': 'Array', 'value': 'array'},
                {'label': 'Range', 'value': 'range'}
            ],
            clearable=False,
            value=kind
        ),
        *inputs
    ])


def feather_icon(name: str):
    return html.I(**{"data-feather": name})


layout = html.Div(className="flex mx-6 my-4 max-h-screen justify-between", children=[
    html.Div(className="w-4/12 max-h-full", children=[
        html.H1(className="text-3xl font-bold", children="System Observer"),
        html.Div(className="px-8 mt-5", children=html.Img(src="/assets/system.png", alt="system graph")),
        html.H2(className="text-xl mt-3 font-bold", children="System"),
        html.Div(children=[
            html.Div(className=functions, children=[
                html.Span(className="text-md", children="Plant"),
                dcc.Input(id="plant_raw", className=input_class, value="1/(s+3)"),
            ])
        ]),
        html.Div(children=[
            html.Div(className=functions, children=[
                html.Span(className="text-md", children="Controller"),
                dcc.Input(id="controller_raw", className=input_class, value="(s+2*x)/(s+4)"),
            ])
        ]),
        html.Div(children=[
            html.Div(className=functions, children=[
                html.Span(className="text-md", children="Feedback"),
                dcc.Input(id="feedback_raw", className=input_class, value="1"),
            ])
        ]),
        html.H2(className="text-xl mt-8 mb-3 font-bold", children="Variable"),
        html.Div(id="var-x-container", className="w-auto",
                 children=construct_variable_definer("range", "x", values=[1.0, 2.5, 0.5])),
        html.H2(className="text-xl mt-8 mb-3 font-bold", children=[
            html.Div(className="flex align-middle",
                     children=["Code",
                               html.Button(id="execute-btn",
                                           className="ml-auto px-2 py-1 text-base rounded-md bg-purple-300",
                                           children="Execute")
                               ])
        ]),
        html.Div(id="code-container", className="w-auto",
                 children=[dash_editor_components.PythonEditor(id='code', value=code_start)]),
        dcc.Textarea(id="code-output-exec",
                     className="flex flex-col w-full h-24 p-2 bg-gray-300",
                     readOnly=True)
    ]),
    html.Div(className="w-1/12 max-h-full flex justify-center", children=[
        html.Button(id="compute-btn",
                    style={"height": "fit-content"},
                    className="mt-4 px-2 py-1 rounded-md bg-green-200 items-center text-center",
                    children=[html.Div(feather_icon("play")), html.Span("Compute")]),
    ]),
    html.Div(className="w-7/12 max-h-full", children=[
        html.Div(className="w-full items-center flex justify-center flex-col", children=[
            html.Div(id="time-graphics", className="w-1/3 mb-3", children=[
                dcc.Dropdown(id="time-graphic-selection",
                             className="",
                             clearable=False,
                             options=[
                                 {'label': "Step Response", 'value': 'step'},
                                 {'label': "Ramp Response", 'value': 'ramp'},
                                 {'label': "Parabola Response", 'value': 'parabola'},
                                 {'label': "Custom Response", 'value': 'custom'},
                             ],
                             value="step")
            ]),
            html.Div(children=[
                dcc.Graph(id="time-plot"),
            ]),
        ]),
        html.Div(className="w-full items-center flex justify-center flex-col", children=[
            html.Div(id="frequency-graphics", className="w-1/3 mb-3", children=[
                dcc.Dropdown(id="freq-graphic-selection", clearable=False,
                             options=[
                                 {'label': "Open Loop Bode", 'value': 'open-bode'},
                                 {'label': "Closed Loop Bode", 'value': 'closed-bode'},
                                 {'label': "Nyquist Plot", 'value': 'nyquist'},
                                 {'label': "Root Locus Plot", 'value': 'rlocus'},
                             ],
                             value="closed-bode")
            ]),
            html.Div(children=[
                dcc.Graph(id="freq-mag-plot"),
                dcc.Graph(id="freq-phase-plot")
            ]),
        ]),
    ]),
])
