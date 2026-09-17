import streamlit as st

from miano_uma_income import DailyTaskIncome, EventIncome, StoryIncome, ExistingCarats
from miano_uma_teamtrials import TeamTrialsIncome, DAYS
from miano_uma_gacha_rates import CharacterBanner, SupportCardBanner, PULL_COST, PITY_PULLS, PITY_COST
from miano_uma_pity import PityCalculator
from miano_uma_simulator import GachaSimulator
from miano_uma_utils import format_carats, format_percent

st.set_page_config(page_title="Uma Musume Carat Toolkit", page_icon="🐴")

if "screen" not in st.session_state:
    st.session_state.screen = "home"


def go_to(screen):
    st.session_state.screen = screen


def back_button():
    if st.button("Back to Home"):
        go_to("home")


def home_screen():
    st.title("Uma Musume Carat & Gacha Toolkit")
    st.write("Pick a tool:")
    if st.button("Carat Income Calculator"):
        go_to("income")
    if st.button("Pity / Probability Calculator"):
        go_to("pity")
    if st.button("Character Banner Simulator"):
        go_to("sim_character")
    if st.button("Support Card Banner Simulator"):
        go_to("sim_support")


def income_screen():
    st.header("Carat Income Calculator")
    back_button()

    existing = st.number_input("Carats you currently have", min_value=0, value=0, step=100)
    story_left = st.number_input("Unclaimed story carats left", min_value=0, value=0, step=10)
    event_carats = st.number_input("Estimated carats from current/upcoming events", min_value=0, value=0, step=50)
    daily_rate = st.number_input("Estimated carats per day from dailies", min_value=0, value=75, step=5)

    st.subheader("Team Trials")
    tt_class = st.selectbox("Your current Team Trials class", options=[1, 2, 3, 4, 5, 6], index=3)
    today = st.selectbox("What day is it today?", options=DAYS)
    days_ahead = st.number_input("Days until your goal (banner end date, etc.)", min_value=1, value=7, step=1)

    if st.button("Calculate total projected Carats"):
        sources = [
            ExistingCarats(existing),
            StoryIncome(story_left),
            EventIncome(event_carats),
            DailyTaskIncome(daily_rate),
        ]
        total = sum(source.calculate(days_ahead) for source in sources)

        tt_income = TeamTrialsIncome(tt_class, today, days_ahead).calculate()
        total += tt_income

        st.success(f"Projected total: {format_carats(total)} by then")
        st.write("Breakdown:")
        for source in sources:
            st.write(f"- {source.name}: {format_carats(source.calculate(days_ahead))}")
        st.write(f"- Team Trials (Class {tt_class}, weekly resets counted): {format_carats(tt_income)}")
        st.caption(f"That's enough for {total // PULL_COST} single pulls.")


def pity_screen():
    st.header("Pity / Probability Calculator")
    back_button()

    banner_choice = st.radio("Which banner?", ["Character (Horse)", "Support Card"])
    banner = CharacterBanner() if banner_choice == "Character (Horse)" else SupportCardBanner()
    calc = PityCalculator(banner)

    st.caption(
        f"Rate-up chance: {format_percent(banner.featured_rate)} per pull  |  "
        f"Guaranteed exchange at {PITY_PULLS} pulls ({format_carats(PITY_COST)})"
    )

    carats = st.number_input("Carats you have available", min_value=0, value=15000, step=150)
    num_pulls = carats // PULL_COST
    st.write(f"That's **{num_pulls} pulls**.")

    chance = calc.chance_by_pulls(num_pulls)
    st.metric("Chance of getting the featured unit at least once", format_percent(chance))

    st.subheader("Planning ahead")
    target = st.slider("Target confidence (%)", min_value=10, max_value=100, value=80) / 100
    pulls_needed = calc.pulls_for_confidence(target)
    st.write(
        f"Pulls needed for {int(target * 100)}% confidence: **{pulls_needed}** "
        f"({format_carats(calc.carats_for_pulls(pulls_needed))})"
    )

    st.subheader("Getting multiple copies")
    st.caption(
        "Rough estimate only (expected value, ignoring the pity reset each banner). "
        "Support cards need 5 total copies for Max Limit Break; horses need extra "
        "copies too, varying by their base rarity."
    )
    n_copies = st.number_input("Copies needed", min_value=1, value=5, step=1)
    est_pulls = calc.expected_pulls_for_copies(n_copies)
    st.write(
        f"Expected pulls for {n_copies} copies: **{est_pulls}** "
        f"({format_carats(calc.carats_for_pulls(est_pulls))})"
    )


def simulator_screen(banner, title, key):
    st.header(title)
    back_button()

    carats = st.number_input("Carats to spend", min_value=0, value=1500, step=150, key=key + "_carats")
    sim = GachaSimulator(banner)

    if st.button("Pull!", key=key + "_pull"):
        num_pulls, tally = sim.simulate_from_carats(carats)
        st.write(f"Simulated **{num_pulls} pulls**:")
        for tier, count in tally.items():
            st.write(f"- {tier}: {count}")


def sim_character_screen():
    simulator_screen(CharacterBanner(), "Character Banner Simulator", "char")


def sim_support_screen():
    simulator_screen(SupportCardBanner(), "Support Card Banner Simulator", "supp")


SCREENS = {
    "home": home_screen,
    "income": income_screen,
    "pity": pity_screen,
    "sim_character": sim_character_screen,
    "sim_support": sim_support_screen,
}

SCREENS[st.session_state.screen]()
