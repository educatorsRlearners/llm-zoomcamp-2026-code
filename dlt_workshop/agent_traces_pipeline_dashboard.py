import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import dlt
    return alt, dlt, mo


@app.cell
def _(dlt):
    pipeline = dlt.attach("agent_traces_pipeline")
    dataset = pipeline.dataset()
    return dataset, pipeline


@app.cell
def _(mo):
    mo.md("# Agent Traces Report")
    return


@app.cell
def _(mo):
    mo.md("## Message Activity Over Time")
    return


@app.cell
def _(dataset):
    df_chart1 = dataset("""
        SELECT
            DATE_TRUNC('hour', timestamp) AS hour,
            COUNT(*) AS message_count
        FROM logs
        GROUP BY 1
        ORDER BY 1
    """).df()
    return (df_chart1,)


@app.cell
def _(alt, df_chart1, mo):
    _chart = alt.Chart(df_chart1).mark_line(point=True).encode(
        x=alt.X("hour:T", title="Hour"),
        y=alt.Y("message_count:Q", title="Messages"),
        tooltip=["hour:T", "message_count:Q"]
    ).properties(title="Message Activity Over Time")
    _chart
    return


@app.cell
def _(mo):
    mo.md("## Model Usage Breakdown")
    return


@app.cell
def _(dataset):
    df_chart2 = dataset("""
        SELECT
            message__model AS model,
            COUNT(*) AS message_count
        FROM logs
        WHERE message__model IS NOT NULL
        GROUP BY 1
        ORDER BY 2 DESC
    """).df()
    return (df_chart2,)


@app.cell
def _(alt, df_chart2, mo):
    _chart = alt.Chart(df_chart2).mark_bar().encode(
        x=alt.X("model:N", title="Model", sort="-y"),
        y=alt.Y("message_count:Q", title="Messages"),
        tooltip=["model:N", "message_count:Q"]
    ).properties(title="Model Usage Breakdown")
    _chart
    return


@app.cell
def _(mo):
    mo.md("## Activity by Project")
    return


@app.cell
def _(dataset):
    df_chart3 = dataset("""
        SELECT
            cwd AS project,
            COUNT(*) AS message_count
        FROM logs
        GROUP BY 1
        ORDER BY 2 DESC
    """).df()
    return (df_chart3,)


@app.cell
def _(alt, df_chart3, mo):
    _chart = alt.Chart(df_chart3).mark_bar().encode(
        x=alt.X("project:N", title="Project", sort="-y"),
        y=alt.Y("message_count:Q", title="Messages"),
        tooltip=["project:N", "message_count:Q"]
    ).properties(title="Activity by Project")
    _chart
    return


if __name__ == "__main__":
    app.run()
