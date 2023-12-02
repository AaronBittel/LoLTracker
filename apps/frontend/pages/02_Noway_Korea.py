import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys, os

sys.path.append(os.getcwd())
from apps.frontend.components import sidebar


def main():
    st.title("Noway Korea SoloQ")

    df = load_data(r"apps/data/dataframes/정신력남자.parquet")

    selected_option = sidebar.create_sidebar(
        text="Analytics",
        options=["Mentality Check", "In game", "Out of game", "Funny", "Educational"],
    )

    match selected_option:
        case "Mentality Check":
            mentality_check(df)
        case "In game":
            in_game(df)
        case "Out of game":
            out_of_game(df)
        case "Funny":
            funny(df)
        case "Educational":
            educational(df)


@st.cache_data
def load_data(path: str):
    return pd.read_parquet(path)


def mentality_check(df: pd.DataFrame):
    st.header("Mentality Check")


def in_game(df: pd.DataFrame):
    st.header("In Game")


def out_of_game(df: pd.DataFrame):
    st.header("Out of Game")


def funny(df: pd.DataFrame):
    st.header("Funny")
    with st.expander("Winrate by deaths"):
        # Add a radio button to select the plotting option
        plot_option = st.radio(
            "Select Plotting Option:",
            ["Only Deaths -> Winrate", "Deaths -> Occurrences", "Both"],
        )

        # Original bar chart (percentage of wins for each number of deaths)
        grouped_data = (
            df.groupby("deaths")["win"].value_counts(normalize=True)[:, True] * 100
        )

        # Count occurrences of death numbers
        death_counts = df["deaths"].value_counts()

        # Create a figure and axes
        fig, ax1 = plt.subplots(figsize=(8, 6))

        # Conditionally plot based on the selected option
        if plot_option == "Only Deaths -> Winrate":
            # Line graph for the percentage of wins
            ax1.plot(
                grouped_data.index,
                grouped_data,
                color="blue",
                marker="o",
                label="Percentage of Wins",
                linestyle="-",
                linewidth=2,
            )
            ax1.set_ylabel("Percentage of Wins", color="blue")
            ax1.tick_params("y", colors="blue")
            ax1.legend(loc="upper left")
        elif plot_option == "Deaths -> Occurrences":
            # Bar chart for occurrences of death numbers
            ax1.bar(
                death_counts.index,
                death_counts,
                color="green",
                alpha=0.7,
                label="Death Counts",
            )
            ax1.set_ylabel("Count", color="green")
            ax1.tick_params("y", colors="green")
            ax1.legend(loc="upper left")
        elif plot_option == "Both":
            # Bar chart for occurrences of death numbers
            ax1.bar(
                death_counts.index,
                death_counts,
                color="green",
                alpha=0.7,
                label="Death Counts",
            )
            ax1.set_ylabel("Count", color="green")
            ax1.tick_params("y", colors="green")

            # Create a second y-axis for the line graph
            ax2 = ax1.twinx()

            # Line graph for the percentage of wins
            ax2.plot(
                grouped_data.index,
                grouped_data,
                color="blue",
                marker="o",
                label="Percentage of Wins",
                linestyle="-",
                linewidth=2,
            )
            ax2.set_ylabel("Percentage of Wins", color="blue")
            ax2.tick_params("y", colors="blue")
            ax2.legend(loc="upper right")

        # Set common x-axis label
        ax1.set_xlabel("Number of Deaths")

        # Display the plot in Streamlit
        st.pyplot(fig)

        st.markdown("Conclusion: **10-Deaths-powerspike** exists!")


def educational(df: pd.DataFrame):
    st.header("Educational")


if __name__ == "__main__":
    main()
