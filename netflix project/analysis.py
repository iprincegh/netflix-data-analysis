from matplotlib import pyplot as plt
import seaborn as sb
import pandas as pd
from textblob import TextBlob

pd.options.mode.chained_assignment = None


#
def _graph_plots(data, filename, x=None, y=None, type=None, xlabel='', ylabel='', title='', figY=6.4, figX=4.8,
                 labels=None, hue=None, kind='box', row=None, aspect=5.6, height=3):
    fig, ax = plt.subplots(figsize=(figY, figX))

    if type == 'heatmap':
        sb.heatmap(data=data, ax=ax)
    elif type == 'barplot':
        sb.barplot(data=data, y=y, x=x, ax=ax, hue=hue)
    elif type == 'pie':
        plt.pie(data=data, x=x, labels=labels, colors=sb.color_palette(), autopct='%.0f%%')
    elif type == 'line':
        sb.lineplot(data=data, x=x, y=y, hue=hue, ci=None, legend="full", palette='Set2',
                    style='type')
    elif type == 'catplot':
        a = sb.catplot(data=data, kind=kind, x=x, y=y, row=row, palette='Set3', sharey=True, aspect=aspect,
                       height=height)
        a.fig.suptitle(title)

    else:
        pass
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    plt.savefig('graphs/{}.pdf'.format(filename))


def create_heatplot(raw_data, filename):
    _graph_plots(data=raw_data.isna(), filename=filename, type='heatmap', xlabel='Columns', ylabel='Id',
                 title="Count of null values in columns", figY=10.4, figX=10.4)


def netflix_ratings(df, plot_filename, csv_filename):
    rating = df.groupby(['rating']).size().reset_index(name='counts')
    _graph_plots(data=rating, filename=plot_filename, type='barplot', x='counts', y='rating', xlabel='Total Counts',
                 ylabel='Ratings', title="Available Netflix Ratings", figY=16, figX=15)
    rating.to_csv('csv_files/{}'.format(csv_filename))


def movies_vrs_series(df, plot_filename):
    dftypes = df['type'].value_counts()
    _graph_plots(data=dftypes, x=dftypes.values, filename=plot_filename, type='pie', labels=dftypes.index,
                 title="Number of Movies and TV shows in the dataset")


def content_prod_trend(df, plot_filename, csv_filename):
    df = df[['type', 'release_year']]
    df = df.rename(columns={"release_year": "Release Year"})
    df = df.groupby(['Release Year', 'type']).size().reset_index(name='Total Content')
    df = df[df['Release Year'] >= 2010]
    _graph_plots(data=df, filename=plot_filename, type='line', x="Release Year", y="Total Content", hue='type',
                 xlabel='Released Year', ylabel='Total Content', title="Netflix content production trend over the years",
                 figY=12, figX=12)
    df.to_csv('csv_files/{}'.format(csv_filename))


def content_sentiment(df, plot_filename, csv_filename):
    df = df[['release_year', 'description']]
    for index, row_val in df.iterrows():
        descr = row_val['description']
        testimonial = TextBlob(descr)
        polarity = testimonial.sentiment.polarity
        if polarity == 0:
            sentiment = 'Neutral'
        elif polarity > 0:
            sentiment = 'Positive'
        else:
            sentiment = 'Negative'
        df.loc[index, 'Sentiment'] = sentiment
    df = df.groupby(['release_year', 'Sentiment']).size().reset_index(name='total_content')
    df = df[df['release_year'] >= 2010]

    _graph_plots(data=df, filename=plot_filename, x='release_year', y='total_content', type='barplot',
                 xlabel='Release Year', ylabel='Total Content', title="Sentiment of content on Netflix", figY=10.4,
                 figX=10.4, hue='Sentiment')
    df.to_csv('csv_files/{}'.format(csv_filename))


class MovieStats:

    def __init__(self, dataframe, group_by_movie=True):
        self.dataframe = dataframe

        if group_by_movie:
            self._group_by_movie()
        else:
            pass

    def _remove_item(self, x) -> int:
        if x == 'No item specified':
            return 0
        return x

    def _group_by_movie(self):
        self.dataframe = self.dataframe[self.dataframe['type'] == 'Movie']
        self.dataframe['duration'] = self.dataframe.duration.map(lambda x: self._remove_item(x.rstrip('min'))).astype(
            int)

    def basic_stats(self, sort_column='director', value_column='date_added', float_point=2):
        df = self.dataframe[[sort_column, value_column]].value_counts().reset_index()

        df_median = df.groupby(sort_column).median()
        df_median = df_median.rename(columns={value_column: 'median'}).reset_index()

        df_mean = df.groupby(sort_column).mean().round(1)
        df_mean = df_mean.rename(columns={value_column: 'mean {}'.format(value_column)}).reset_index()

        df_std = df.groupby(sort_column).std()
        df_std = df_std.rename(columns={value_column: 'std'}).reset_index()

        df = pd.merge(df_mean, df_std, on=[sort_column])
        df = pd.merge(df, df_median, on=[sort_column])[[sort_column, 'mean {}'.format(value_column), 'std', 'median']]
        df.sort_values(by=sort_column, inplace=True, ascending=False)
        df.to_csv('csv_files/mean-std-median of {}-{} columns.csv'.format(sort_column, value_column))

    def distribution_plots(self, plot_filename, y_column, x_column, labels=[], kind='box'):
        df = self.dataframe[[x_column, y_column]].value_counts().reset_index().rename(columns={0: 'count'})
        countries = df[x_column].unique().tolist()[:8]

        df = df[df[x_column].isin(countries)]
        df = df[~df[x_column].isin(['No item specified'])]

        _graph_plots(data=df, filename=plot_filename, type='catplot', kind=kind, x=x_column, y=y_column,
                     xlabel=labels[0], ylabel=labels[1], title=labels[2], aspect=2, height=6)
