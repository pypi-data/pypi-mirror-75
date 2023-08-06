import dash
import sympy as sp
import numpy as np
import control2020 as ct20
import control as ct
import sys
import contextlib
from io import StringIO

from dash.dependencies import Input, Output, State

from .labo import BasicExperiment, BasicSystem, Variable, normalized_tf
from .layout import layout, construct_variable_definer
from .utils import state_to_variable
from .templates import index_template


@contextlib.contextmanager
def stdout_io(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


exp = BasicExperiment(BasicSystem(ct.TransferFunction([1], [1, 1, 1])))
exp.add_variable(Variable("x", kind="range", start=0, end=5, step=1))

external_stylesheets = [
    "https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css"
]

external_scripts = [
    "https://unpkg.com/feather-icons",
    "https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"
]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
)

app.index_string = index_template
app.layout = layout


# app.renderer = renderer

@app.callback(Output("time-plot", "figure"),
              [Input("compute-btn", "n_clicks"),
               Input("time-graphic-selection", "value")],
              [State("plant_raw", "value"),
               State("controller_raw", "value"),
               State("feedback_raw", "value"),
               State("var-x-container", "children")])
def render_time(clicks, plot_type, plant_raw, controller_raw, feedback_raw, current_var):
    s = state_to_variable(current_var)
    exp.update_var(s.name, s)

    if plot_type == "step":
        t = np.linspace(0, 30, 250)
        u = np.ones_like(t)
        return exp.render_time_any(t, u, g=plant_raw, k=controller_raw, h=feedback_raw)
    elif plot_type == "ramp":
        t = np.linspace(0, 50, 250)
        u = t
        return exp.render_time_any(t, u, g=plant_raw, k=controller_raw, h=feedback_raw)
    elif plot_type == "parabola":
        t = np.linspace(0, 50, 250)
        u = np.square(t)
        return exp.render_time_any(t, u, g=plant_raw, k=controller_raw, h=feedback_raw)

    t = np.linspace(0, 50, 250)
    u = np.ones_like(t)
    return exp.render_time_any(t, u, g=plant_raw, k=controller_raw, h=feedback_raw)


@app.callback([Output("freq-mag-plot", "figure"),
               Output("freq-phase-plot", "figure")],
              [Input("compute-btn", "n_clicks"),
               Input("freq-graphic-selection", "value")],
              [State("plant_raw", "value"),
               State("controller_raw", "value"),
               State("feedback_raw", "value"),
               State("var-x-container", "children")])
def render_freq(clicks, plot_type, plant_raw, controller_raw, feedback_raw, current_var):
    s = state_to_variable(current_var)
    exp.update_var(s.name, s)

    if plot_type == "closed-bode":
        return exp.render_bode(g=plant_raw, k=controller_raw, h=feedback_raw)
    elif plot_type == "open-bode":
        return exp.render_bode(g=plant_raw, k=controller_raw, h=feedback_raw, feedback_kind="open")

    return exp.render_bode(g=plant_raw, k=controller_raw, h=feedback_raw)


@app.callback(Output("var-x-container", "children"),
              [Input("var-kind-select", "value"),
               Input("var-name", "value")],
              [State("var-x-container", "children")])
def update_variable_params(kind, name, current_var):
    final_var = current_var

    if name != "":
        var = state_to_variable(current_var)
        current_kind = var.kind

        current_once = var.fixed or 0.0
        current_array = var.fixed or [0.0]
        current_start = var.start or 0.0
        current_end = var.end or 1.0
        current_step = var.step or 1.0

        if kind == current_kind:
            if kind == "once":
                final_var = construct_variable_definer(kind, name, [current_once])
            elif kind == "array":
                final_var = construct_variable_definer(kind, name, current_array)
            elif kind == "range":
                final_var = construct_variable_definer(kind, name, [current_start, current_end, current_step])
        else:
            final_var = construct_variable_definer(kind, name)

    return final_var


@app.callback(Output("code-output-exec", "value"),
              [Input("execute-btn", "n_clicks")],
              [State("var-name", "value"),
               State("plant_raw", "value"),
               State("controller_raw", "value"),
               State("feedback_raw", "value"),
               State("code", "value")])
def execute_code(clicks, var_name, g, k, h, code):
    zero_sys = exp.new_system(var_name, "0.0", g, k, h)
    with stdout_io() as s:
        try:
            exec(code, {
                "np": np,
                "sp": sp,
                "ct": ct,
                "ct20": ct20,
                "G": zero_sys.G,
                "K": zero_sys.K,
                "H": zero_sys.H
            })
        except:
            print("Something wrong with the code")
    string_out = s.getvalue()
    outs = string_out.split("\n")
    out = "\n".join([out for out in outs if out != ""])
    return out
