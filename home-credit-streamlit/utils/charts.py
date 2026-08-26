import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# LINE CHART
# ==========================================================
def line_chart(df:pd.DataFrame,data_col:str,value_col:str,title:str,freq:str="ME"):
    data=(df.groupby(pd.Grouper(key=data_col,freq=freq))[value_col].sum().reset_index())
    fig=px.line(data,x=data_col,y=value_col,title=title,markers=True)
    return fig

# ==========================================================
# MULTI LINE CHART
# =========================================================
def multi_chart(df:pd.DataFrame,data_col:str,value_cols:list,title:str,freq:str="ME"):
    data=(df.groupby(pd.Grouper(key=data_col,freq=freq))[value_cols].sum().reset_index())
    fig=px.line(data,x=data_col,y=value_cols,title=title,markers=True)
    return fig

# ==========================================================
# BAR CHART
# ==========================================================
def bar_chart(df:pd.DataFrame,group_col:str,value_col:str|None,title:str,top_n:int=None,aggfunc:str="sum"):
   if value_col is None:
       data=(df.groupby(group_col).size().reset_index(name="value"))
       sort_col="value"
   else:
       if aggfunc=="sum":
            data=(df.groupby(group_col)[value_col].sum().reset_index())
       elif aggfunc=="mean":
            data=(df.groupby(group_col)[value_col].mean().reset_index())
       elif aggfunc=="count":
            data=(df.groupby(group_col)[value_col].nunique().reset_index())
       else:
            data=(df.groupby(group_col)[value_col].sum().reset_index())
       sort_col=value_col
   data = data.sort_values(
        sort_col,
        ascending=False
    )

   if top_n is not None:
        data = data.head(top_n)

   fig = px.bar(data,x=group_col,y=sort_col,title=title,text=sort_col)

   return fig    

# ==========================================================
# HORIZONTAL BAR CHART
# ==========================================================
def horizontal_bar_chart(df: pd.DataFrame,group_col: str,value_col: str,title: str,top_n: int = None):

    data = (
        df.groupby(group_col)[value_col]
        .sum()
        .reset_index()
    )

    data = data.sort_values(
        value_col,
        ascending=True
    )

    if top_n is not None:
        data = data.tail(top_n)

    fig = px.bar(
        data,
        y=group_col,
        x=value_col,
        orientation="h",
        title=title
    )

    return fig


# ==========================================================
# PIE CHART
# ==========================================================

def pie_chart(
    df: pd.DataFrame,
    names_col: str,
    title: str
):

    data = (df[names_col].value_counts() .reset_index())

    data.columns = [names_col,"Count"]

    fig = px.pie(data,names=names_col, values="Count",title=title)

    return fig

# ==========================================================
# DONUT CHART
# ==========================================================
def donut_chart(
    df: pd.DataFrame,
    names_col: str,
    title: str
):

    data = (
        df[names_col]
        .value_counts()
        .reset_index()
    )

    data.columns = [
        names_col,
        "Count"
    ]

    fig = px.pie(
        data,
        names=names_col,
        values="Count",
        hole=0.5,
        title=title
    )

    return fig

# ==========================================================
# HISTOGRAM
# ==========================================================
def histogram(
    df: pd.DataFrame,
    column: str,
    title: str,
    bins: int = 30
):

    fig = px.histogram(
        df,
        x=column,
        nbins=bins,
        title=title
    )

    return fig


# ==========================================================
# SCATTER CHART
# ==========================================================
def scatter_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: str | None,
    title: str
):

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        hover_data=df.columns
    )

    return fig

# ==========================================================
# BOX PLOT
# ==========================================================

def box_plot(
    df: pd.DataFrame,
    y_col: str,
    x_col: str | None,
    title: str
):

    fig = px.box(
        df,
        y=y_col,
        x=x_col,
        title=title
    )

    return fig


# ==========================================================
# VIOLIN PLOT
# ==========================================================
def violin_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str
):

    fig = px.violin(
        df,
        x=x_col,
        y=y_col,
        box=True,
        title=title
    )

    return fig

# ==========================================================
# HEATMAP
# ==========================================================

def heatmap(
    data: pd.DataFrame,
    title: str
):

    fig = go.Figure(
        data=go.Heatmap(
            z=data.values,
            x=data.columns,
            y=data.index
        )
    )

    fig.update_layout(title=title)

    return fig

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================
def correlation_heatmap(
    df: pd.DataFrame,
    columns: list,
    title: str
):

    corr_matrix = df[columns].corr()

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r"
    )

    fig.update_layout(title=title)

    return fig


# ==========================================================
# WATERFALL CHART
# ==========================================================
def waterfall_chart(
    df: pd.DataFrame,
    category_col: str,
    value_col: str,
    title: str
):

    data = (
        df.groupby(category_col)[value_col]
        .sum()
        .reset_index()
    )

    fig = go.Figure(
        go.Waterfall(
            x=data[category_col],
            y=data[value_col],
            textposition="outside",
            text=data[value_col]
        )
    )

    fig.update_layout(title=title)

    return fig
# ==========================================================
# DEFAULT RATE CHART
# ==========================================================
def default_rate_chart(
    df: pd.DataFrame,
    group_col: str,
    title: str
):

    data = (
        df.groupby(group_col)["TARGET"]
        .mean()
        .reset_index()
    )

    data["Default Rate %"] = (
        data["TARGET"] * 100
    )

    fig = px.bar(
        data,
        x=group_col,
        y="Default Rate %",
        color="Default Rate %",
        title=title
    )

    return fig

# ==========================================================
# MISSING VALUE CHART
# ==========================================================

def missing_values_chart(
    df: pd.DataFrame,
    top_n: int = 20
):

    missing = (
        df.isnull()
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        x=missing.index,
        y=missing.values,
        title="Top Missing Value Columns"
    )

    return fig


# ==========================================================
# RISK GAUGE CHART
# ==========================================================
def risk_gauge(
    score: float,
    title: str = "Risk Score"
):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": title},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "red"}
            }
        )
    )

    return fig