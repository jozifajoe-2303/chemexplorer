import streamlit as st
import requests
from urllib.parse import quote

st.set_page_config(
    page_title="ChemExplorer",
    page_icon="🧪",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #06152e, #0b2850);
    color: #f2f7ff;
}
h1, h2, h3, p, label {
    color: #f2f7ff !important;
}
[data-testid="stMetric"] {
    background: #12365e;
    border: 1px solid #2878bb;
    padding: 16px;
    border-radius: 12px;
}
.stButton > button {
    background: #1685e5;
    color: white;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.title("🧪 ChemExplorer")
st.caption("Explore molecules. Discover chemistry.")

st.markdown(
    "### Molecular Research Explorer\n"
    "Search a molecule to explore its chemical properties."
)

molecule = st.text_input(
    "🔎 Search molecule",
    placeholder="Try Water, Glucose or Caffeine"
)

if st.button("Explore Molecule"):
    if not molecule.strip():
        st.warning("Please enter a molecule name.")
    else:
        name = quote(molecule.strip(), safe="")
        url = (
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
            f"compound/name/{name}/property/"
            "MolecularFormula,MolecularWeight,IUPACName,"
            "CanonicalSMILES,XLogP,TPSA,HBondDonorCount,"
            "HBondAcceptorCount,RotatableBondCount/JSON"
        )

        try:
            response = requests.get(url, timeout=20)

            if response.status_code == 200:
                props = response.json()["PropertyTable"]["Properties"][0]

                st.success("Molecule found!")
                st.header(molecule.title())

                st.markdown("#### Chemical structure")
                image_url = (
                    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"
                    f"compound/name/{name}/PNG"
                )
                img = requests.get(image_url, timeout=20)

                if img.status_code == 200:
                    st.image(img.content, width=300)

                st.markdown("#### Molecular properties")

                fields = [
                    ("Molecular formula", "MolecularFormula"),
                    ("Molecular weight (g/mol)", "MolecularWeight"),
                    ("IUPAC name", "IUPACName"),
                    ("Canonical SMILES", "ConnectivitySMILES"),
                    ("XLogP", "XLogP"),
                    ("TPSA (Å²)", "TPSA"),
                    ("H-bond donors", "HBondDonorCount"),
                    ("H-bond acceptors", "HBondAcceptorCount"),
                    ("Rotatable bonds", "RotatableBondCount"),
                ]

                for label, key in fields:
                    value = props.get(key)
                    if value is None and key == "ConnectivitySMILES":
                        value = props.get("SMILES")
                    st.markdown(
                        f"**{label}:** "
                        f"{value if value is not None else 'Not available'}"
                    )

                cid = props.get("CID")
                if cid:
                    st.link_button(
                        "View full PubChem record",
                        f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}"
                    )

                st.caption("Data source: PubChem")

            elif response.status_code == 404:
                st.error(
                    "Molecule not found. Check the spelling "
                    "or try a common chemical name."
                )
            else:
                st.error(
                    "The database is temporarily unavailable. "
                    "Please try again."
                )

        except requests.RequestException:
            st.error("Network issue. Please try again later.")
        except (KeyError, IndexError, ValueError):
            st.error("Could not read the molecule data.")

st.divider()
st.caption("ChemExplorer | A chemistry learning project")
