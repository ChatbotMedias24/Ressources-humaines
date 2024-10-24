import streamlit as st
import openai
import streamlit as st
from dotenv import load_dotenv
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from streamlit_chat import message  # Importez la fonction message
import toml
import docx2txt
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
import docx2txt
from dotenv import load_dotenv
if 'previous_question' not in st.session_state:
    st.session_state.previous_question = []

# Chargement de l'API Key depuis les variables d'environnement
load_dotenv(st.secrets["OPENAI_API_KEY"])

# Configuration de l'historique de la conversation
if 'previous_questions' not in st.session_state:
    st.session_state.previous_questions = []

st.markdown(
    """
    <style>

        .user-message {
            text-align: left;
            background-color: #E8F0FF;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: 10px;
            margin-right: -40px;
            color:black;
        }

        .assistant-message {
            text-align: left;
            background-color: #F0F0F0;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: -10px;
            margin-right: 10px;
            color:black;
        }

        .message-container {
            display: flex;
            align-items: center;
        }

        .message-avatar {
            font-size: 25px;
            margin-right: 20px;
            flex-shrink: 0; /* Empêcher l'avatar de rétrécir */
            display: inline-block;
            vertical-align: middle;
        }

        .message-content {
            flex-grow: 1; /* Permettre au message de prendre tout l'espace disponible */
            display: inline-block; /* Ajout de cette propriété */
}
        .message-container.user {
            justify-content: flex-end; /* Aligner à gauche pour l'utilisateur */
        }

        .message-container.assistant {
            justify-content: flex-start; /* Aligner à droite pour l'assistant */
        }
        input[type="text"] {
            background-color: #E0E0E0;
        }

        /* Style for placeholder text with bold font */
        input::placeholder {
            color: #555555; /* Gris foncé */
            font-weight: bold; /* Mettre en gras */
        }

        /* Ajouter de l'espace en blanc sous le champ de saisie */
        .input-space {
            height: 20px;
            background-color: white;
        }
    
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar contents
textcontainer = st.container()
with textcontainer:
    logo_path = "medi.png"
    logoo_path = "NOTEPRESENTATION.png"
    st.sidebar.image(logo_path,width=150)
   
    
st.sidebar.subheader("Suggestions:")
questions = [
        "Donnez-moi un résumé du rapport ",
        "Quels sont les principaux objectifs du Projet de Loi de Finances pour l'année 2025 ?",
        "Quelles mesures sont prévues pour améliorer l'efficacité des services publics en termes de gestion des ressources humaines ?",
        "Comment le gouvernement prévoit-il de moderniser les processus de recrutement et de gestion du personnel ?",
        "Comment le rapport envisage-t-il l'utilisation des nouvelles technologies dans la gestion des ressources humaines ?"
]
# Initialisation de l'historique de la conversation dans `st.session_state`
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = StreamlitChatMessageHistory()
def main():
    text="""
1ERE PARTIE: Transformation de l’Administration
publique, un enjeu constant, une détermination
indéfectible et des choix qui se confirment

La réforme de l'Administration publique, fortement impulsée par les Hautes Orientations
Royales, figure au centre des préoccupations du Gouvernement. Elle vise prioritairement à
instaurer une action publique centrée sur le citoyen, à implémenter des modes innovants de
management et d'organisation, ainsi qu'à améliorer la qualité et l'efficacité des services
publics.

A la lumière de cet engagement, le Gouvernement a propulsé la stratégie Maroc Digital 2030
en tant que levier central de réforme des services publics, un choix qui ne suggère
aucunement une renonciation aux projets structurants faisant partie intégrante du socle sur
lequel repose la transformation globale de l'Administration.

Dans cette dynamique réformatrice, le Gouvernement accorde une attention particulière à la
préservation et à la pérennisation de la paix sociale, en faisant du dialogue social un puissant
levier institutionnel de valorisation des ressources humaines et de stimulation de leur
performance.

l. LE DIALOGUE SOCIAL : OUTIL REMARQUABLE DE RÉGULATION
DES RELATIONS DE TRAVAIL ET DE VALORISATION DES
RESSOURCES HUMAINES

Résolus à prévenir les conflits, à désamorcer les facteurs de tension et à préserver les acquis
économiques et sociaux du pays, le Gouvernement et les partenaires économiques et
sociaux s'accordent sur la nécessité de construire un dialogue social institutionnalisé. Ce
dialogue doit reposer sur une démarche de négociation et définir les responsabilités de
chacun des acteurs qui y sont engagés.

Le dialogue social engagé en 2024 a été de portée centrale formalisée dans les mesures
prises dans le cadre du dialogue social central, et sectorielle à travers les mesures décidées
dans le cadre du dialogue social sectoriel relatives particulièrement aux secteurs de
l'Education Nationale et de la Santé.

1. Dialogue social central, avancée significative pour la consolidation de la
paix sociale: accord du 29 Avril 2024

Soucieux de contenir les tensions sociales et de motiver la classe des travailleurs (secteur
public et secteur privé), le Gouvernement a scellé, le 29 Avril 2024, un accord avec les
partenaires économiques et sociaux, et ce, dans le cadre du dialogue social central. L'accord
tripartite conclu prévoit la batterie de mesures suivantes :

> Mesures portant sur l'amélioration du revenu :
+ Secteur public
o Augmentation mensuelle nette de 1.000 DH, à verser en 2 tranches
égales (ler Juillet 2024, ler Juillet 2025), des rémunérations des

Aù

personnels de l'Etat, des collectivités territoriales et des établissements
publics qui n’ont pas encore bénéficié de révision salariale.

Il est à souligner que les textes de mise en œuvre de la revalorisation des salaires des
fonctionnaires ont été publiés au bulletin officiel n° 7320 du 25 Juillet 2024 et la première
tranche a été payée.

e Secteur privé
o Augmentation de 10% du SMIG (Salaire Minimum Interprofessionnel
Garanti) appliquée en deux tranches (5 % au ler Janvier 2025 et 5% au ler
Janvier 2026) ;
o Augmentation de 10% du SMAG (Salaire Minimum Agricole Garanti)
appliquée en deux tranches (5 % au 1er Avril 2025 et 5 % au ler Avril 2026).

Le Gouvernement prévoit également, suite à cet accord, une révision de l’Impôêt sur le
Revenu (IR), et ce, à compter du ler Janvier 2025.

> Autres mesures :
L'accord porte aussi sur les mesures suivantes :

+ Réforme des systèmes de retraite: il est question d'instaurer un régime de
retraite selon deux pôles (public et privé) dont les modalités seront établies
dans le cadre d’une approche participative en préservant les droits acquis dans
les systèmes de retraite actuels et en renforçant la gouvernance de ces
systèmes en se référant aux bonnes pratiques reconnues dans ce domaine ;

° Elaboration de la loi organique relative aux conditions et aux modalités de
l'exercice du droit à la grève ;

° Révision de la législation du travail à travers ce qui suit :

o Révision progressive de certaines dispositions du code du travail sur la
base d’une démarche participative visant à assurer un équilibre entre la
productivité de l’entreprise et la préservation de sa compétitivité ;

o Révision du cadre réglementaire et institutionnel régissant la formation
professionnelle continue.

2. Dialogue social sectoriel du Ministère de PEducation Nationale (MEN): accords du 14
Janvier 2023, du 10 et 26 Décembre 2023

Le Gouvernement affiche un intérêt marqué pour l'opérationnalisation de la feuille de route
relative à la réforme de l’école publique ; un engagement qui vise la mise en place d'une
école publique de qualité offrant de meilleures perspectives pour l'élève, et valorisant le rôle
de l'enseignant. Dans cette optique, le Gouvernement à conclu trois accords, à savoir
l'accord du 14 Janvier 2023 et les accords du 10 et 26 Décembre 2023, avec les syndicats de
l'Education Nationale les plus représentatifs. Ces accords s’articulent autour des principaux
points suivants :

e Mise en place d'un nouveau statut particulier unifié et motivant régissant à la fois les
fonctionnaires du Ministère et ceux des Académies Régionales d'Education et de
Formation ;

+ Amélioration des conditions matérielles de l'ensemble du personnel du MEN à travers
une augmentation générale mensuelle nette des salaires statutaires de 1.500 DH
répartie en deux tranches (1 Janvier 2024, 1 Janvier 2025) ;

AN

RAPPORT SUR LES RESSOURCES HUMAINES

e Création d’un grade supplémentaire (Hors Echelle) et octroi d'années de bonification
au profit du personnel dont le parcours professionnel s'arrête à l'échelle T1;

e Revalorisation, et institution, des indemnités complémentaires au profit de certaines
catégories de personnel du MEN.

Les textes relatifs à ces mesures ont été publiés au bulletin officiel n° 7277 du 26 Février
2024 et la première tranche de l'augmentation susmentionnée a été servie en Avril 2024.

3. Dialogue social sectoriel du Ministère de la Santé et de la Protection Sociale: accord
du 23 Juillet 2024.

Conscients du rôle primordial et pertinent du dialogue social dans l'instauration d’une paix
sociale pérenne et la résolution des conflits sociaux, le Ministère de la Santé et de la
Protection Sociale et les syndicats du secteur ont conclu un accord qui prévoit les mesures
principales suivantes :

e Augmentation mensuelle nette de 500 DH et 200 DH au profit respectivement des
infirmiers et des cadres administratifs, à compter du 1° Juillet 2025, et ce en sus de
l'augmentation de 1000 DH décidée dans le cadre de l'accord de 29 Avril 2024 du
dialogue social central ;

° Accélération de la publication du décret portant institution d’une indemnité de
fonction au profit des professionnels de la Santé chargés de la supervision et de
l'encadrement des stagiaires ;

°« Révision de l'indemnité de garde et d'astreinte pour les professionnels de la Santé ;

e Extension de l'octroi de l'indemnité de risque aux enseignants chercheurs exerçant au
Ministère.

Tenant compte de tous les accords conclus dans le cadre du dialogue social au titre de la
période 2022-2024, le coût annuel global de l’ensemble des mesures prises s’élèverait à près
de 45 milliards de dirhams à l'horizon 2026.

Il. PROJETS STRUCTURANTS DE LA REFORME DE L'ADMINISTRATION
1. La digitalisation: une percée remarquable

La digitalisation à grande échelle a engendré des changements économiques et sociétaux
significatifs. Elle est d’ailleurs présentée par certains courants de pensée comme une
solution à bon nombre de questions de développement et perçue, à ce titre, comme un
impératif et non une simple option. De surcroît, la digitalisation occupe désormais une place
prépondérante dans le fonctionnement des services publics.

1.1. Exploration de quelques indicateurs sur Péconomie numérique à Finternational et au Maroc

Le premier volume des « Perspectives de l'économie numérique de l'OCDE 2024 » apporte
des éclairages édifiants sur la croissance du secteur des Technologies de l'Information et de
la Communication (TIC) dans les pays de l'OCDE. Le rapport souligne que ledit secteur n'a
nullement montré des signes d’'essoufflement au titre de l'année 2023, enregistrant même un
taux de croissance moyen de 7,6%; avec des pays comme le Royaume Uni, la Belgique,
l'Allemagne, l'Autriche et les Pays-Bas qui affichent un niveau de croissance soutenu.

Le rapport « Digitalisation in Europe 2022-2023 » publié en 2023 par la Banque Européenne
d'Investissement (BEI) soulève, de son côté, l'engagement énergique des pays de l’Union

7 N

Européenne dans la transformation numérique. La conception d'un plan de financement de
plus de 165 milliards d'euros au profit de la « Décennie numérique de l’Europe », fixant de
fortes ambitions numériques pour 2030, est à ce titre en parfaite corrélation avec cette
vision.

Pour ce qui est de l'Afrique, le rapport « Afrique numérique : transformation technologique
pour l’emploi » publié en 2023 par la Banque mondiale indique que les technologies
numériques présentent des avantages significatifs pour les personnes et les entreprises, et

augmentent, à cet effet, les opportunités d'emploi pourvu que les investissements en
infrastructures numériques et en ressources humaines soient intensifiés.

Au Maroc, le Gouvernement œuvre au renforcement de la position du pays en tant que hub
numérique en Afrique tirant pleinement parti de la palette d'atouts proposée en termes
d'infrastructures, de connectivité et de potentiel humain. A ce titre, l'édition 2023 de l'indice
GSLI (Global Services Location Index) fait ressortir les performances du Maroc en matière
d'outsourcing. Le Maroc y est présenté comme la 2ème meilleure destination en Afrique et
se positionne à la 4ème place au niveau de la région MENA et à la 28ème au niveau mondial.

Cette conjoncture favorable a permis au Maroc d'attirer un flux considérable
d'investissements et a été récemment confortée par la signature d'un mémorandum
d'entente entre le Gouvernement et le groupe Oracle, leader mondial des technologies de
l'information, pour la création d'un centre de services cloud hyperscale au Maroc. Ce centre
est appelé à assurer des services cloud avancés au Maroc et à l'international.

1.2. Grands axes de la stratégie digitale du Gouvernement

L'agenda numérique du Gouvernement repose dorénavant sur la stratégie Maroc Digital
2030 élaborée dans la perspective de bâtir un écosystème digital pérenne et pertinent,
d'apprécier lucidement les enjeux économiques du digital et d'en cerner les implications
sociétales. Il s'aligne aussi sur la volonté du Gouvernement de prendre le virage
incontournable de la transformation digitale afin de moderniser l'action publique et de
mieux servir le citoyen et l'entreprise.

Deux axes majeurs sont définis dans le cadre de cette stratégie :

Axe 1- La digitalisation des services publics afin de mieux servir les citoyens et les
entreprises (E-Gov)

Cet axe a pour objectifs essentiels de faciliter l'accès aux services publics, de fluidifier les
procédures, de réduire les délais et de simplifier les parcours usagers. || a aussi ambition de
faire figurer le Maroc, d'ici 2030, au top 50 mondial sur l'EGDI (E-Government Development
Index) des Nations Unies qui évalue les niveaux de transformation numérique dans les pays.

A ce titre, les leviers mis en avant, en lien avec cet axe, devraient se focaliser sur :

- Une méthodologie axée sur l'usager ;

- La détermination des rôles et des responsabilités des acteurs concernés notamment
le Ministère de la Transition Numérique et de la Réforme de l'Administration, les
différentes Administrations et l'Agence du Développement du Digital (ADD) ;

- La réglementation adaptée à prévoir ;

- Une inclusion de grande envergure.

AN

RAPPORT SUR LES RESSOURCES HUMAINES

Axe 2- La dynamisation de l’économie numérique en vue de produire des solutions
numériques marocaines et de créer de la valeur et de l'emploi

Cet axe a pour objectif de faire monter en gamme le secteur et de conquérir de nouveaux
marchés. A ce titre, des mesures de forte portée sont prévues, relatives particulièrement
aux volets suivants :

Le développement d’un vivier de talents de qualité ;

- Le positionnement de l'offre national sur les filières à forte valeur ajoutée ;
- La mise en place d’un cadre d'incitations favorable au numérique ;

- La promotion de la destination Maroc à l'International.

De surcroît, et dans le cadre de la stimulation de la production de solutions numériques
marocaines, la stratégie vise à porter le nombre de startups à 3.000 d'ici 2030 contre
environ 380 en 2022. Pour ce faire, des mesures se rapportant à la mise en place d'une
« startup policy », aux plans de financement à envisager, aux mécanismes d'accompagnement
et à l'accès aux marchés sont prévues.

Dans cette même perspective, il est question de dynamiser la digitalisation des entreprises,
d'assurer Un accompagnement du passage à l'échelle des Petites et Moyennes Entreprises
Technologiques marocaines et d'assister les Très Petites, Petites, et Moyennes Entreprises
(TPME) dans leur transformation digitale.

Et afin de garantir une mise en œuvre efficace des différentes composantes de la stratégie
Maroc Digital 2030, trois catalyseurs ont été ciblés à savoir :

1. Les « digital talents » : l'objectif affiché est d'atteindre 100.000 nouveaux talents
(digital talents) par an à l'horizon 2030 à travers la formation de 45.000
talents/an, la reconversion vers les métiers numériques au profit de 50.000
personnes/an et l'attraction de 6.000 talents étrangers par an.

2. Le Cloud; il est question de disposer d'un cloud souverain et d’un cloud public et
d'assurer les offres de services y afférents.

3. La connectivité : la stratégie ambitionne, concernant ce catalyseur, d'assurer une
couverture plus large, d'inclure les zones rurales et éloignées, de garantir une
meilleure qualité de la connectivité et enfin de stimuler le marché y afférent.

Le déploiement de la stratégie Maroc Digital 2030 devrait concomitamment tenir compte de
2 paramètres incontournables à savoir :

> L'énorme potentiel que présente l'Intelligence Artificielle (A) pour l'accompagnement
de la digitalisation des services publics et l'amélioration de la qualité des services rendus
aux citoyens et aux entreprises. Cela passe nécessairement par le renforcement de
l'écosystème de FIA.

> La pertinence d’un Usage numérique inclusif couvrant les différentes zones
géographiques et touchant les différentes catégories de la population. Cela se
traduit, entre autres, par l'intégration des principes d’inclusion numérique dans la
conception des services, l'amélioration de la couverture réseau, la sensibilisation
des citoyens à l'utilisation des services en ligne et une inclusion numérique plus
marquée des femmes.

pN

Il est par ailleurs souligné que la stratégie Maroc Digital 2030 devrait fortement s'appuyer
sur la mobilisation de mécanismes de gouvernance forts et agiles.

1.3. Décryptage de quelques initiatives de digitalisation lancées par le Gouvernement

Le Gouvernement s'emploie à faire du digital un réel levier de développement multisectoriel.
Ainsi et dans le cadre de sa stratégie volontariste de se doter d’une feuille de route pour le
développement de l'innovation digitale, le Gouvernement a signé en 2024 un contrat-
programme ambitieux avec le Maroc Numeric Cluster (MNOC), organisme reconnu pour son
expertise en matière de promotion de l'innovation digitale. Ce contrat-programme se
propose particulièrement de massifier l'offre formation-insertion dans le domaine des
Technologies de l'Information et de stimuler l'écosystème des startups et des «Très Petites
Entreprises» (TPE) et des «Petites et Moyennes Entreprises» (PME).

L'élan digital a également concerné le secteur de l'Education Nationale. Le Gouvernement a,
ainsi, mis en place une plateforme de développement de solutions numériques « Digital Lab »
conçue à des fins pédagogiques et de gestion, et appelée, à ce titre, à répondre aux besoins
des professeurs, des élèves et des établissements d'enseignement.

S'agissant du secteur de la Santé, le Gouvernement à coiffé en 2024 la signature d'une
convention-cadre de partenariat pour le déploiement de solutions numériques à laquelle ont
adhéré le Ministère de la Santé et de la Protection sociale, le MTNRA, l'Agence Nationale de
Réglementation des Télécommunications (ANRT), la Caisse Nationale de Sécurité Sociale
(CNSS) et l'Agence de Développement du Digital (ADD). Cette convention-cadre vise, à
travers les solutions numériques susmentionnées, à assurer une plus grande fluidité du suivi
médical, une meilleure coordination entre les professionnels de la Santé et une simplification
des procédures de remboursement des frais de soins médicaux. Elle s'inscrit pleinement dans
la dynamique de restructuration du secteur de la santé engagée par le Gouvernement. Sa
pertinence découle, à cet effet, de sa conformité avec la loi-cadre n° 06.22 relative au système
national de santé, notamment les dispositions se rapportant à la digitalisation de ce système.

Déterminé aussi à répondre aux attentes du citoyen dans le domaine de la justice et à
renforcer la performance de l’action judiciaire, le Gouvernement à engagé des actions visant
l'unification, la simplification et la numérisation de l'Administration judiciaire. Le portail
« mahakim.ma » a ainsi enregistré, en 2023, près de 23 millions de visiteurs uniques.

L'engagement du Gouvernement en matière de transformation digitale dans le système
judiciaire a été également confirmé par l'organisation, les 8 et 9 Février 2024 à Tanger,
d'une conférence internationale sous le thème « La transformation digitale du système
judiciaire: vecteur d'une justice efficiente et inclusive » en collaboration avec le Programme
des Nations Unies pour le Développement (PNUD).

Dans le secteur du Commerce, il y a surtout lieu de relever l'apport de la plateforme
«Moroccan Retail Tech Builder : MRTB », fruit d’un travail coordonné entre le Gouvernement et
quelques partenaires, en matière d’incubation de startups porteuses de projets de solutions
digitales en lien avec le secteur du Commerce au Maroc.

De surcroît, Le Gouvernement affiche sa volonté de booster l'activité touristique au Maroc
en exploitant les outils numériques. Il a, à cet effet, supervisé en 2024 le cadre de partenariat

AN

RAPPORT SUR LES RESSOURCES HUMAINES

stratégique scellé entre L'ADD, la Société Marocaine d'Ingénierie Touristique (SMIT) et la
Fédération Marocaine des Technologies de l'Information, des Télécommunications et de
l'Offshoring (APEBI. Ce partenariat, couvrant la période 2024-2026, porte sur la
digitalisation des services touristiques via la promotion des investissements y afférents. Il est
d’ailleurs prévu, au titre de ce partenariat, d'apporter un soutien aux petites et moyennes
entreprises attirées par l'investissement dans le digital lié au tourisme.

14. L'Agence du Développement du Digital (ADD) : catalyseur de la stratégie digitale du
Gouvernement

L'ADD à été créée en vertu de la loi n° 61.16 publiée au Bulletin Officiel n° 6622 du 16
Novembre 2017. L'ADD, qui opère sous tutelle du département en charge de la Transition
Numérique, est investie de la mission d'exécution de la stratégie du Gouvernement en
matière de développement du digital. Elle est, au titre des prérogatives qui lui sont
conférées, chargée de la structuration de l'écosystème du digital notamment à travers la
promotion du « Smart Gouvernement » axé sur la digitalisation des services publics, la
stimulation de l'économie digitale et de la compétitivité des entreprises, le renforcement de
la dynamique de la recherche et de l'innovation et l'accélération de l'inclusion digitale via les
outils numériques.

La feuille de route de l’ADD s'articule autour de 15 chantiers notamment « l'écosystème
dédié à l'intelligence artificielle », « l'appui à l’évolution du cadre réglementaire » en lien avec
le digital, « Génération digitale » et « Digital auto-entrepreneur ». Le plan d'action de l'ADD
établi en 2024 se focalise sur le soutien devant être apporté au Gouvernement sur bon
nombre d'actions particulièrement :

e La digitalisation des parcours administratifs en se basant sur l’interopérabilité ;

+ Le développement de la plateforme e-learning « Academia Raqmya» en y intégrant de
nouveaux programmes de formation en faveur du grand public, des Administrations
et des entreprises (TPE, PME et Startups) ;

e L'amélioration de la plateforme « Moukawala Raqgmya » qui présente un système
d'auto-évaluation de la maturité digitale des Très petites, Petites et Moyennes
Entreprises marocaines et propose l'accompagnement adapté ;

+ L'amélioration de la plateforme « startuphub» dans le souci de dématérialiser les
demandes des entreprises opérant dans les domaines des nouvelles Technologies de
l'Information et de la Communication (NTIC) et souhaitant obtenir le label «Jeunes
entreprises innovantes en nouvelles technologies ».

1.5. GITEX : vitrine de promotion de l'innovation digitale

Le Maroc a organisé du 29 au 31 Mai 2024 à Marrakech, la seconde édition du Salon GITEX
Africa, un événement technologique marquant auquel 1500 entreprises internationales ont
pris part. Le GITEX se veut une plateforme de promotion de l'innovation digitale et conforte
l'engagement du Maroc sur la voie de la transformation digitale en Afrique. Cette édition a
particulièrement mis en relief la prépondérance de l'intelligence artificielle au regard de ses
impacts économiques avérés. Elle a été aussi marquée par l'organisation de débats autour
des défis numériques en Afrique.

Aù

Il est à rappeler que la première édition du GITEX AFRICA, également tenue à Marrakech, du
31 Mai au 2 Juin 2023, a surtout mis l'accent sur la promotion de l'innovation technologique
multisectorielle et de la digitalisation. En marge de cet événement, des conventions
renforçant l’interministérialité digitale ont été actées.

2. La déconcentration administrative: de bonnes perspectives

Dès la publication du décret n°2-17-618 (26 Décembre 2018) portant charte nationale de la
déconcentration administrative et du décret n°2-19-40 (24 Janvier 2019) fixant le schéma
directeur référentiel de la déconcentration administrative, les efforts sont déployés pour
réussir ce chantier stratégique. Ainsi, le bilan de la feuille de route de la déconcentration
administrative se présente comme suit :

°e L’approbation, au cours de l'année 2019, de 23 schémas directeurs de la
déconcentration administrative pour 22 départements ministériels et pour le
Haut-Commissariat au Plan ;

e La publication de l'arrêté du Ministre de l'Intérieur n°2782/19 fixant l’organisation du
Secrétariat Général des Affaires Régionales (SGAR) et la nomination des Secrétaires
Généraux des Affaires Régionales ;

° L'inclusion des fonctions de «Chefs des Représentations Administratives Régionales
Sectorielles » et de « Chefs de Représentations Administratives Communes » parmi les
fonctions nommées par le Conseil de Gouvernement (modification de la loi organique
n°02-12 relative à la nomination aux fonctions supérieures) ;

+ La diffusion de la circulaire du Chef de Gouvernement n° 17/2020 pour activer la
feuille de route relative à la mise en œuvre de la déconcentration administrative à
travers cinq axes principaux : la révision de l'organisation des départements
ministériels, le renforcement et la qualification des ressources humaines et financières
des services déconcentrés, la clarification des compétences à transférer aux services
déconcentrés soit par la délégation de pouvoir, soit par la délégation de signature, le
renforcement des mécanismes de suivi et de gouvernance, et l'accompagnement par
un programme national de formation et de communication ;

e La mise en place d’une commission chargée de préparer une matrice contenant les
décisions de gestion des ressources humaines à déléguer ou à transférer aux services
déconcentrés, le calendrier de leur mise en œuvre et la liste des textes législatifs et
réglementaires relatifs à la gestion des ressources humaines à réviser ;

°e La publication du décret n° 2.22.81 (30 Mars 2023) relatif à la délégation de pouvoir et
de signature au bulletin officiel n°7187 du 30/03/2023 (édition arabe);

° La préparation des projets de décrets suivants :

o Un projet de décret relatif aux principes et règles d'organisation des
administrations de l'État et fixant leurs attributions (approuvé au Conseil de
Gouvernement le 2 Mai 2024) ;

o Un projet de décret relatif aux modalités de nomination des chefs de division et
des chefs de service au sein des Administrations publiques (reporté par le
Conseil de Gouvernement susmentionné).

e Le transfert de 15 actes relatifs à l'investissement, sur Un total de 44, aux services
déconcentrés ;

e Le développement d'une plateforme numérique pour la gestion et le suivi de la mise
en œuvre des schémas directeurs de la déconcentration administrative ;

AN

RAPPORT SUR LES RESSOURCES HUMAINES

e L'approbation, par la Commission interministérielle de la Déconcentration administrative,
de la configuration finale des représentations administratives communes et sectorielles
au niveau régional, en date du 19 Juin 2023;

e L'élaboration, par la Commission Technique chargée de la mise en œuvre de la Charte
de la déconcentration administrative, en concertation avec les départements
concernés, de trois projets de décrets portant création et organisation des
représentations administratives communes au niveau régional et relatives à
« la production industrielle et extractive, aux services et à l'insertion économique », à
« l'équipement et aux infrastructures », au « tourisme, à l'artisanat, à l'économie
sociale et solidaire, à la jeunesse, à la culture et à la communication ».

> Prochaines étapes de ce chantier :

e La poursuite de la mise en œuvre du cadre législatif et réglementaire relatif à la
déconcentration administrative, notamment la publication des projets de
décrets sus-indiqués ;

° L'accélération du transfert des actes d'investissement aux services déconcentrés
et de la publication des textes législatifs et réglementaires y afférents ;

°e La révision des structures administratives des services centraux et déconcentrés
pour les aligner sur les attributions définies dans les schémas directeurs de la
déconcentration administrative ;

°e L’actualisation et l'approbation des schémas directeurs de la déconcentration
administrative.

3. La simplification des procédures administratives

Conscient de la nécessité de reconfigurer les relations de l'Administration avec le citoyen et
l'investisseur et d'améliorer l'accessibilité aux services publics, le Gouvernement a élaboré en
2020 la loi n° 55-19 relative à la simplification des procédures et des formalités administratives.
Un dispositif réglementaire d'appui a été également mis en place incluant particulièrement :

+ Le décret n° 2.20.660 du 18 Septembre 2020 en application de quelques dispositions
de la loi n° 55-19 ;

e Le décret n° 2.22.141 du 8 Mai 2023 relatif à l'application de certaines dispositions de
la loi n° 55-19, portant sur la simplification des procédures et des formalités
administratives, concernant les actes administratifs délivrés par les Collectivités
Territoriales, leurs groupements et leurs instances ;

e Le décret n° 2.22.385 du 8 Mai 2023 relatif à la fixation de la liste des décisions
administratives nécessaires pour la réalisation des projets d'investissement dont le
délai de traitement des demandes y afférentes ne dépasse pas 30 jours.

A ce titre, nombreuses sont les actions qui ont été entreprises par le Gouvernement pour
simplifier les parcours administratifs et renforcer la promptitude du fonctionnement de
l'Administration en prenant appui sur la digitalisation. Cet engagement a été fortement
formalisé à travers la mise en œuvre de plusieurs portails notamment le Portail national des
procédures et des formalités administratives (ID ARATI), le Portail national des réclamations
(Chikaya), le Portail de transparence et accès à l'information (Chafafiya), le Portail de
géolocalisation des Services publics, le Portail de l'Emploi public et le Centre d'appel et

d'orientation administrative.

Aù

Sur la même voie et eu égard à l'ambition du Gouvernement d'attirer les investissements et
de faciliter les parcours et les démarches y afférents, la plateforme électronique CRI-INVEST
a été mise en place.

4. La consolidation du caractère officiel de la langue amazighe : un engagement qui
prend forme

Le Gouvernement s'implique vivement dans l'application de la feuille de route relative à la
mise en œuvre du caractère officiel de la langue amazighe couvrant un large éventail de
mesures touchant principalement l'Administration, les services publics, la justice,
l'enseignement, la culture et l'audiovisuel. A ce titre, 300 millions de DH ont été prévus pour
ce chantier dans le cadre de Loi de Finances 2024.

De surcroit et dans le cadre de l'engagement manifeste du Gouvernement pour l'intégration
de la langue amazighe dans les institutions publiques, des conventions ont été signées en
2024 entre plusieurs départements ministériels et institutions publiques à travers lesquelles il
a été question de doter quelques administrations publiques d'agents chargés d'orienter le
public amazighophone. || est également prévu d'introduire la langue amazighe dans 10 sites
web officiels des Administrations publiques.

Il est à souligner que le 14 Janvier (nouvel an amazigh) a été décrété jour férié national
officiel au Maroc.

Il. AXES D'ACTION MAJEURS DE LA BONNE GOUVERNANCE

1. Engagement du Maroc dans Flinitiative multilatérale du Partenariat pour un
Gouvernement Ouvert : une confirmation

Fort de son dynamisme dans l'Initiative multilatérale du Partenariat pour un Gouvernement
Ouvert notamment en matière de transparence budgétaire et d’intégrité, le Maroc à été
reconduit pour un second mandat au niveau du comité de pilotage pour une période de 3
ans à compter du ler Octobre 2024, et ce, à l'instar du Royaume-Uni et de l'Estonie.

Et dans le cadre de la consolidation de ces acquis, le 3ème Plan d'Action National
2024-2027, a été engagé à travers le lancement d’une consultation publique en Avril 2024
sur les projets d'engagements à proposer, et comprenant 12 engagements articulés autour
de la transparence, de l'égalité et de l'inclusion, de l'espace civique, de la justice ouverte, et
des collectivités territoriales ouvertes.

2. La lutte contre la corruption : un chantier perfectible

En vue d’enrayer la corruption et d'assurer l'immunité morale du service public, et après la
création de l'instance Nationale de la Probité, de la Prévention et de la Lutte contre la
Corruption (INPPLC) en vertu de l’article 36 de la Constitution et la publication de la loi
n°113.12 abrogée et remplacée par la loi n°46.19, le Gouvernement a déployé la Stratégie
Nationale de Lutte Contre la Corruption visant la moralisation de là vie publique et la
consolidation des principes de la bonne gouvernance.

Ad

RAPPORT SUR LES RESSOURCES HUMAINES

Sur cette lancée de grande portée, le Gouvernement prévoit aussi d'élaborer des loi relatives
à la déclaration du patrimoine et à la lutte contre toute forme d'enrichissement illicite, à la
prévention et à la lutte contre les conflits d'intérêts de même qu'à la protection des
fonctionnaires signalant des actes de corruption ; en plus d’un projet de décret portant
charte des valeurs et d'éthique du fonctionnaire dans les Administrations publiques, les
Collectivités Territoriales et les Etablissements publics.

En 2023 le Maroc a obtenu le score de 38 sur 100 dans l’Indice de Perception de la
Corruption (IPC) conçu par « International Transparency », se classant ainsi au 97ème rang
sur 180 pays et territoires. À souligner que l'IPC classe les pays et les territoires sur une
échelle de zéro (forte corruption) à 100 (aucune corruption).

Il est à souligner que l'INPPLC a publié son rapport d'activité, au titre de l’année 2023,
présentant un diagnostic détaillé de la situation de la corruption aux niveaux international,
régional et national. Le rapport s’attelle aussi à évaluer les stratégies et politiques déployées
en matière de lutte contre la corruption. || présente également des recommandations et
propositions visant à développer l’action de l'instance et à assurer un suivi optimal de ses
différentes recommandations en matière de lutte contre la corruption.

2EME PARTIE : RESSOURCES HUMAINES DE LA
FONCTION PUBLIQUE MAROCAINE

I. EVOLUTION DE LA POPULATION ET DES EFFECTIFS DU PERSONNEL
CIVIL DE L'ETAT AU COURS DE LA PERIODE 2014-2024

1. Evolution de la population et des effectifs du personnel civil de FEtat
1.1. Evolution de la population

Le Maroc a enregistré en l’espace d’une décennie des variations démographiques
significatives avec une population maintenant son trend haussier passant de 33,77 millions
d'habitants en 2014 à 37,37 millions d'habitants en 2024 et affichant de ce fait une
croissance de 10,66% au titre de cette période et une progression additionnelle moyenne de
360.014 habitants par an. L'évolution de la population marocaine au titre de la période 2014-
2024 est illustrée par le graphique suivant :

Figure 1 : Evolution de la population marocaine pour la période 2014-2024

[ # Li Population Rurale 4 [={ | Population à
2024 24. 387 12. 983 { 37.370
2023 23.991 13.031 { 37. 022
2022 23.592 13.079 { 36.670
2021 23. 189 13.124 { 56.313
2020 22. 783 13.168 w | 35. 952
ny 20 22.376 13. 211 { 35.587
d 2018 21. 968 13. 251 { 35.220
£ 207 21. 561 13. 292 { 34. 852
2016 21. 5 13.332 { 34.487
2015 20. 752 13.373 { 34.125
2014 20. 353 13. 417 À 53 7702. ja4a
L J

A signaler la montée en puissance de la proportion de la population urbaine entre 2014 et
2024, dûe en partie à l'exode rural et à l'urbanisation des zones rurales. Les villes marocaines
abriteraient 65,3% des habitants du Royaume au terme de l’année de 2024, au lieu de 60,3%
enregistré en 2014. La population rurale connaîtrait, en revanche, un léger recul de son
effectif.

Le taux d'accroissement annuel démographique durant la période 2014-2024, a enregistré
une décélération de 0,23 point en passant de 117% en 2014 à 0,94% en 2024, enregistrant
ainsi un taux annuel moyen de la période considérée de 1,02%, soit un taux qui avoisine le
taux d’'accroissement démographique annuel de la population mondiale qui est de près de
1%.

PN

RAPPORT SUR LES RESSOURCES HUMAINES

Par ailleurs, l'évolution de la population active entre le deuxième trimestre de l’année 2014 et
celui de 2024 s’est traduite par une croissance moyenne d'environ 48.500 actifs additionnels
par an pour atteindre 12,49 millions de personnes en 2024, soit un taux de croissance annuel
moyen de 0,40% par an. Cette croissance est essentiellement urbaine avec un taux de 2,2%
par an, contre un repli observé au niveau de la population rurale d'un taux de 2,03% par an.

Figure 2 : Evolution de la population marocaine active au cours de la période 2014-2024
(Données 2°" trimestre)

[ [Population active Urbaine |E4] | Population active Rurale { LE | Population active {
2024 4.524 { 12.490
2023 4.624 { 12.482
2022 4.765 { 12. 411
2021 4.954 { 12. 497
2020 4.640 { 11.964
2019 4. 975 { 12.057
$ 2018 5.287 { 2178
£ 2017 5. 253 { 12. 081
2016 5. 203 { 11.974
2015 5.545 { 11. 970
2014 5.598 { 12.005 , 4000
NS J

Source: Données de l'Enquête Nationale de l'Emploi, HCP.
1.2. Evolution des effectifs du personnel civil de l'Etat

Au Maroc, le marché d'emploi se caractérise par son hétérogénéité et par une contribution
remarquable de l'État en tant qu'employeur public, traduisant la volonté et l'engagement des
pouvoirs publics de dynamiser le marché de l'emploi à travers le mécanisme de création des
postes budgétaires, et de répondre aux besoins de l'administration en ressources humaines
nécessaires à l'amélioration de la qualité des services publics et des prestations rendus aux
citoyens et aux acteurs économiques.

En 2024, la fonction publique marocaine compte 570.917 fonctionnaires civils, soit un taux
d'administration de 15,3%. Ainsi en moyenne, 15 fonctionnaires civils sont au service de
1.000 personnes, et près de 48 fonctionnaires pour 1.000 habitants de la population active.
Le tableau qui suit renseigne amplement sur ces tendances :

Population totale 33.770.000 37.370.000
Population active 11.677.000 11.983.000
Effectif du personnel civil 578.057 570.917
D ISO du personnel civil sur Population 1,71% 153%
Ratio Effectif du personnel civil sur Population 495% 176%

active

NN

Durant la période 2014-2024, le taux de couverture des fonctionnaires civils par rapport à la
population totale et à la population active s'élève respectivement à 1,61% et 4,77% en
moyenne tout en entamant une tendance bâaissière à partir de 2016.

Figure 3 : Part des effectifs des fonctionnaires civils au sein de la population marocaine et de la population
marocaine active au cours de la période 2014-2024

f NS
198% | Ratio Effectif Ratio Effectif du - 5,20%
: du personnel civil sur ] L personnel civil
à # Ve Population
2 _ Se macive + 5,00%
1,88% - f ]
4,95%
+ 4,80%
178% - 4 | 4,76%
1,71% #1, , j 4,72% | 460%
1,68% -
- 4,40%
159% 158% 57%
158% | LS4% 153% 153% | 4,20%
1,48% T T T T T T T T T T T 4,00%
LU 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025

A

L'effectif budgétaire du personnel civil de l'Etat est passé de 578.057 en 2014 à 570.917 en
2024 enregistrant, ainsi une régression globale d'environ 1,24%.

Cette légère tendance à la baisse enregistrée depuis l'année 2016, est le résultat de l'effet
conjugué de l'opération de recrutement des enseignants au niveau des Académies
Régionales de l'Education et de la Formation (AREF) depuis cette année!, et des départs
massifs à la retraite, pour limite d'âge ou anticipée, notamment du personnel du Ministère de
l'Éducation Nationale.

Figure 4 : Evolution de l'effectif budgétaire civil au cours de la période 2014-2024

[ ù
2024 570.917
2023 565.252
2022 565.429
2021 570.877
a 2020 568.920
É 201 564.592
< 2018 568.769
2017 570.603
2016 583.267
2015 585.503
2014 D - 578.057
Effectif Civil
L J

? Au cours de la période 2016-2024, 159.000 enseignants ont été recrutés au niveau des AREFS

Ad

L'évolution de l'effectif des fonctionnaires civils de l'État est le résultat de l'effet combiné
des opérations de création et de suppression des postes budgétaires. Ces opérations
peuvent être influencées par plusieurs facteurs tels que les politiques Gouvernementales, les
besoins du service public et les contraintes budgétaires.

Le Gouvernement a procédé, dans le cadre de la loi de finances 2024, à la création de
30.034 postes budgétaires au profit des ministères et institutions suivants :

Le Chef du Gouvernement est habilité à répartir 500 postes budgétaires entre les différents
départements ministériels ou institutions, dont 200 postes sont réservés au recrutement des
personnes en situation d’handicap.

En 2024, les départements de l'Intérieur, de la Défense Nationale, et de la Santé et de la
Protection Sociale s'accaparent 68% de l’ensemble des postes créés au titre de cette année.
En effet la priorité a été accordée aux départements de sécurité et ceux à caractère social

pour satisfaire leur besoin en ressources humaines nécessaires.

L'examen de l’évolution des créations des postes budgétaires permet d’avoir une vision sur
les orientations Gouvernementales en matière de dotation en ressources humaines
nécessaires aux secteurs prioritaires.

Figure 5 : Evolution des créations des postes budgétaires pour la période 2014-2024

[ 2024 30.054

2023 28.272

2022 26.860
2021

2020

2019

Années

2018

2017

2016

2015

2014 17.975

KL )

Au titre de la période 2014-2024, il a été procédé à la création de 264.812 postes
budgétaires, auxquels s'ajoutent 159.000 postes créés au niveau des Académies Régionales
de l'Education et de la Formation (AREF) pour le recrutement des enseignants du primaire
et du secondaire selon les années scolaires comme suit :

Année 2016/ | 2017/ | 2018/ | 2019/ | 2020/ | 2021/ | 2022/ | 2023/ | 2024/ Total
2017 2018 2019 | 2020 | 2021 2022 | 2023 | 2024 2025

Postes
budgétaires
créés au niveau

11.000 24.000 20.000 15.000 15.000 17.000 17.000 20.000 20.000 159.000

des AREFS

AU titre de la période 2014-2024, la priorité en termes de créations de postes budgétaires a
été accordée aux départements sociaux et de sécurité. En effet, 63% des postes créés ont
été affectés aux départements de l'Intérieur, de l'Education Nationale et de l'Enseignement
Supérieur, et de la Santé.

La structure de la répartition de ces créations, par département, au titre de la période
précitée se présente comme suit :

A

RAPPORT SUR LES RESSOURCES HUMAINES

Figure 6 : Structure des créations des postes budgétaires par département au titre de la période 2014-2024

[ n
Habous et Affaires
Islamiques
2%
Justice
1%
Economie et ______ Intérieur
Finances | 31%
3% |
aération D NE
Pénitentiaire _
3%
Enseignement
Supérieur
Ne 4% J

L'analyse de ce graphique au titre de la période 2014-2024 fait ressortir les constats
suivants :

° Plus de 31% des postes budgétaires créés, soit 82.690 postes, ont été affectés au

Ministère de l'Intérieur et ce, afin de doter les différents services de sécurité de
moyens humains nécessaires pour qu'ils s'’acquittent des missions qui leur
incombent en matière de maintien de l'ordre public et de la sécurité des citoyens ;
En sus des 159.000 postes créés au profit des enseignants recrutés aux AREFS, 12%
et 4% des postes budgétaires créés, soit 31.626 postes et 10.962 postes ont été
octroyés respectivement aux départements de l'Education Nationale et de
l'Enseignement Supérieur;

Le département de la Santé, vu l'importance qu'il cristallise dans l’action
Gouvernementale, a bénéficié de 41.500 postes, ce qui représente près de 16% du
total des créations observées durant la période considérée ;

Les départements de l'Economie et des Finances ainsi que l'Administration
Pénitentiaire ont bénéficié au titre de la même période d'un renforcement de leur
capital humain respectivement de 8.974 et 7.150 postes budgétaires, ce qui
représente près de 6% du total des créations observées durant la période
considérée;

D'un autre côté, les créations de postes budgétaires par groupes d’échelles au titre de la
période 2014-2024, se déclinent comme suit :

Figure 7 : Evolution des Créations des postes budgétaires par groupe d'échelles
au cours de la période 2014-2024

\
lro0% -
90% - à
ES x
Oo ES Ft R ©
80% | £ | Q 8 . Fe ë Le) & à
& œ : L Ÿ Ÿ
DER te Li Lo»
60% - L6%.4 ef V4 |
12%
15%
40% + |:5,1 L_\ y ”.
œ@ Q
30% | = 2 ES a & R ë . e
e & CD an in à © © Ex
20% + MM Ê S Le Ÿ
le] N
10% - D,
0% +
2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024
e HEchelle 6 et assimilé  MEchelles 7 à 9  MEchelles 10 et plus
J

L'analyse des créations des postes par groupes d’échelles pour la période considérée fait
ressortir ce qui suit :

e Le nombre total des postes créés pour le recrutement des cadres (échelles 10 et
plus) au sein des différents départements s'élève à 101.607 postes, ce qui
représente 38,4% de la totalité des créations intervenues au cours de cette
décennie, avec une moyenne annuelle de 9.237 postes ;

+ Pour le personnel de maîtrise classé aux échelles 7 à 9, le nombre de postes créés
est de 26.647 postes budgétaires, soit 10% du total des créations, avec une
moyenne annuelle de 2.422 postes ;

e Le nombre de postes budgétaires créés et réservés au personnel d'exécution
classé à l'échelle 6 et assimilés à atteint au titre de ladite période 136.557 postes
budgétaires, soit 51,6% du nombre total des créations intervenues au titre de cette
période, affichant ainsi une moyenne annuelle de 12.414 de postes.

2.2. Suppressions des postes budgétaires

Les départs à la retraite constituent le principal facteur de suppression des postes
budgétaires puisqu'ils ont généré près de 82% des suppressions effectuées au niveau des
différents départements durant la période 2014-2024.

Les graphiques ci-après retracent l'évolution et la répartition par départements des
suppressions des postes budgétaires en raison de départs à la retraite et des suppressions
des postes vacants au cours de la période 2014-2024 :

A

RAPPORT SUR LES RESSOURCES HUMAINES

Figure 8 : Evolution des Suppressions des postes budgétaires au cours de la période 2014-2024

NS
[ 2024 15.754

2023 14.120
2022

2021
2020

2019

Années

2018

2017

2016

2015

2014 14.811

L )

Figure 9 : Structure des suppressions des postes budgétaires par départements pour l& période 2014-2024

f Santé à
11%

Education : *

Nationale D \ Economie et
62% fi Finances

3%

Agriculture

Enseignement Intérieur
Supérieur 8%
NE 4% /

L'examen de ces graphiques fait ressortir les observations suivantes :

+ 62% des postes budgétaires supprimés au cours de la période considérée relèvent
du département de l'Education Nationale, soit 119.028 postes supprimés ;

e Les départements de la Santé, de l'Intérieur, de l'Enseignement Supérieur, de
l'Economie et Finances, et de l'Agriculture ont accusé respectivement 11%, 8%, 4%,
3% et 1% de l’ensemble des suppressions intervenues au titre de la période
considérée, soit respectivement la suppression de 22.138 postes, 15.317 postes,
8.457 postes, 5.865 postes et 2.451 postes durant ladite période ;

e Par ailleurs, les suppressions effectuées au niveau des autres départements
représentent 19.719 postes supprimés, soit près de 10% de l’ensemble des

suppressions enregistrées pendant cette même période.

S'agissant des suppressions de postes par groupes d'échelles au titre de la période 2014-
2024, elles se déclinent comme suit :

Figure 10 : Structure des suppressions des postes budgétaires par groupes d'échelles
pour la période 2014-2024

18.022
20.389

16.137
13.386

2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024

L HEchelle 6 et assimilé Echelles 7 à 9 LA Echelles 10 et plus D.

+ Les suppressions des postes budgétaires occupés par les cadres (échelles 10 et
plus) représentent 79,5% de l’ensemble des suppressions effectuées au titre de la
période précitée soit 153.493 postes supprimés ;

+ La suppression des postes occupés par le personnel d'exécution (échelle 6 et
assimilés) représente 10,8% du total des suppressions constatées durant la
décennie considérée avec 20.849 postes supprimés ;

+ 9,7% des suppressions ont concerné des postes occupés par le personnel de
maîtrise classé aux échelles 7 à 9 avec 18.633 postes supprimés.

3. Accès à la fonction publique

3.1, Concours de recrutement

La politique de recrutement dans la fonction publique marocaine est fortement imprégnée
des dispositions de l'article 31 de la Constitution consacrant le principe d'égalité des
citoyennes et citoyens pour l'accès aux emplois publics selon le mérite et également des
dispositions de l'article 22 du Statut Général de la Fonction Publique instituant le concours
comme règle générale d'accès à la Fonction Publique.

Ainsi, les départements ministériels ont procédé durant la période allant de l’année 2014
jusqu'à Septembre 2024 à l'annonce de 3.297 concours pour pourvoir 164.050 postes
budgétaires, ce qui représente une moyenne de 50 postes ouverts par concours.

AN

RAPPORT SUR LES RESSOURCES HUMAINES

Figure 11 : Structure des concours publiés et des postes ouverts au recrutement aux services de l'Etat
pour la période 2014-2024

(” Lnapèresesostesaunens 4
26.000 - + 700
24000 | 17e 23.370
22.000 - 1 600
20.000 -
18.000 ! 16192 16.560 17602 1 500
16.000 14.939 v
À 400
14.000 - 11845
12.000 | 300
10.000
8.000 ] 200
6.000
4.000 À 100
2.000 | 167 à
0 < EM Er | il 0

2021 2022 2023 2024

Ne

La répartition par administration, des postes budgétaires ouverts au recrutement et leurs
moyennes par nombres de concours publiés au titre des années 2023 et 2024 se présente
comme suit :

Nombre de Nombre moyen de
Nombre de
p concours postes par
— . —_— postes publiés A A
Administration organisatrice publiés concours publiés
2023 2024 2023 2024 2023 2024
Ministère de l'Intérieur 8.709 8.351 87 77 100 108
Ministère de la Santé et de la Protection Sociale 7.669 4.739 279 125 27 38

Délégation Générale à l'Administration 1.307 1.041 6 7 218 149
Pénitentiaire et à la Réinsertion

1.200 2.584 5 7 240 369

Ministère de l'Agriculture, de la Pêche Maritime, du

Développement Rural et des Eaux et Forêts 254 75° / L . .
Ministère de l'Education Nationale, du Préscolaire 214 4.675 8 10 27 468
et des Sports

Ministère de l'Enseignement Supérieur, de la 156 57 3

Recherche Scientifique et de Finnovation

AN

Ministère des Affaires Etrangères, de la

Coopération Africaine et des Marocains Résidant Br 6 21

à l'Étranger

Ministère de l'Aménagement du Territoire

National, de l'Urbanisme, de l'Habitat et de la 10 17 5 7 2
Politique de la Ville

Ministère de la Jeunesse, de la Culture et de la 103 107 23 28 4 4
Communication

Autres 5

1.120 8

76 5 64 7 18
Par ailleurs, la répartition du nombre de postes ouverts au recrutement et du nombre de

concours publiés par groupes d’échelles, au titre de l’année 2023 et jusqu’à Septembre 2024
peut être illustrée par le tableau ci-après :

Nombre de postes Nombre de concours Nombre moyen de
ubliés publiés EXCEL OI ELTACCECUTE
Groupes P publiés
d'échelles
2023 2024 2023 2024 2023 2024
8.598 8.214 43 21 200 391

3.484 2.512 138 68 25 37

10 et plus 9.700 12.644 421 260 23 49

La répartition, par grade, du nombre de postes budgétaires ouverts au recrutement et du
nombre de concours annoncés à cet effet, au titre de l’année de 2023 jusqu'à Septembre
2024, est détaillée dans le tableau ci-après :

Nombre de postes Nombre de Nombre moyen de
p" . postes par
publiés concours publiés A
concours publiés
2023 2024 2023 2024 2023 2024
Gardien de la paix 4.127 3.437 1 1

Infirmier/Assistant médico-

social/kinésithérapeute/Technicien de 3.376 2.993 85 61 40 49
santé/Sage-femme de premier grade

Administrateur 2ème grade 2.198 1.804 99 A5 22 40
Inspecteur de police 2.050 2.500 1 1 2.050 2.500
Technicien de 3ème grade 1.884 1.498 79 41 24 37

AN

4.127 3.437

RAPPORT SUR LES RESSOURCES HUMAINES

399 5.357 30 35 13 153
CECI ET CIE

3.2. Concours spécial unifié pour le recrutement des personnes en situation de handicap

Conscient de l'ampleur de ce phénomène à l'échelle nationale, le Maroc a ratifié en 2009 la
Convention internationale relative aux droits des personnes handicapées. Le pays à
également adopté une approche inclusive visant à intégrer pleinement les personnes en
situation de handicap dans la société. Cette vision a pris une dimension légale avec
l'adoption de la constitution de 2011, qui consacre dans son préambule l'engagement de

PN

l'État à « bannir et combattre toute discrimination à l'encontre de quiconque, en raison du
sexe, de la couleur, des croyances, de la culture, de l’origine sociale, de la langue, du
handicap ou de toute autre circonstance personnelle ». La loi cadre n° 97-13 relative à la
protection des droits des personnes en situation de handicap a également marqué une
avancée majeure en ce sens.

Afin de concrétiser ces initiatives, notamment dans la fonction publique, le gouvernement a
décidé de réserver un nombre de postes budgétaires aux personnes en situation de
handicap.

À cet effet, il convient de signaler que depuis Décembre 2018, cinq éditions de concours
unifiés de recrutement dans la fonction publique, toutes catégories confondues, ont été
organisées au profit des personnes en situation de handicap. Ces concours se sont déroulés
sous la supervision du Chef du Gouvernement et en coordination avec les services du
Ministère de la Transition Numérique et de la Réforme de l'Administration, du ministère de
l'Économie et des Finances, ainsi que du ministère de la Solidarité, de l'insertion Sociale et de
la Famille, en plus des 14 départements ministériels concernés.

La cinquième édition de ces concours, datée du 25 Février 2024, a ciblé le recrutement de
280 postes d'administrateur troisième grade, 50 postes d'administrateur deuxième grade, 45
postes de technicien troisième grade et 25 postes de technicien quatrième grade, soit un
total de 400 postes budgétaires pour les années 2023 et 2024.

Et afin de permettre aux candidats de passer dans des meilleures conditions leurs examens,
les concours ont été organisés au niveau de quatre centres régionaux, à savoir : Rabat, Fès,
Marrakech et Agadir.

Le tableau suivant récapitule les principaux résultats de cette 5éme édition du concours
unifié :

Candidats admis Taux de
Spécialités réussite des
6
5
4
7
6

Technicien de 4ème Informatique 9 15 40%
grade Gestion

5 10 50%
Informatique 16 20 20%
Gestion

8 15 47%
secrétariat (e) 6 100%

Administrateur 3ème Economie / Droit 43 77 120 36%
grade Lettres / Sciences 47 113 160 29%
Administrateur 2ème Economie / Droit 2 28 30 7%
grade Lettres / Sciences 10 10 20 50%

Depuis le lancement de cette opération en 2018, les administrations publiques ont recruté au
total 1.246 candidates et candidats en situation de handicap et sont répartis par grades
comme suit :

AN

Technicien de 3ème
grade

RAPPORT SUR LES RESSOURCES HUMAINES

- 160 administrateurs de 2°"° grade parmi les titulaires du diplôme de Master ;

- 910 administrateurs de 3°"° grade parmi les titulaires de la licence ;

-_ 116 techniciens de 3°" grade parmi les titulaires du diplôme de technicien spécialisé ;
-__ 60 techniciens de 4°" grade parmi les titulaires du diplôme de technicien.

Par ailleurs, le taux de réussite des femmes suite à ces cinq éditions de concours à connu une
amélioration significative en passant de 18% en 2018 à 33% en 2024.

3.3. Recrutement des experts

Les recrutements d'experts par voie contractuelle sont réalisés conformément au décret n°
2-15-770 du 9 Août 2016, définissant les conditions et modalités de recrutement par contrat
dans les administrations publiques. Ce décret permet aux différents départements de
répondre à leurs besoins en compétences et en expertise dans divers domaines, notamment
pour l'exécution et le suivi des grands projets et des projets structurants.

Dans cette optique, 93 appels à candidatures ont été lancés pour recruter 132 experts depuis
2018 jusqu'à Septembre 2024.

Le graphique ci-après présente la répartition par année de l'effectif de ces experts depuis
l'application du décret sus-indiqué :

Figure 12 : Appels à la candidature pour le recrutement des experts pour la période 2018-2024

( EH Nombre de postes d'experts Li Appels à la candidature à
25 26
21 23 22
16 18
12 13
L 2018 2019 2020 2021 2022 2023 2024 )

4. Nominations aux emplois supérieurs et aux postes de responsabilité
4.1, Nominations aux emplois supérieurs

La nomination aux emplois supérieurs est encadrée par le dahir n° 1-12-20 du 17 Juillet 2012
portant exécution de la loi organique n° 02-12 relative aux nominations aux emplois
supérieurs en application des dispositions des articles 49 et 92 de la constitution sur ces
fonctions.

A ce titre, 1.463 nominations aux emplois supérieurs ont été recensées depuis l’année 2014
jusqu'à Septembre 2024. L'évolution et la répartition de ces nominations par fonction durant

la période considérée se présentent comme suit :

ronetons [2014 | 20152016 | 2017 |zo16 2010 |2020 | 2021/2022 | 2025) 2024 | ou | %
IA CVS 108 82 94 | 61 173 108 92 | 84 | 117 | 140 93 1152 | 788%
Inspecteur ES 5 2 2 13 4 53 | 3,6%
Général
RUES 4 7  o  o 4 6 3  O 2 5 0 31 21%
d'université
Recteur de PORT 2 3 25 24 12 18 11 16 13 166 | 1,3%
faculté

Secrétaire 9 42%
Général

4 2 5 12 6 2 1 7 8 5
rotal [155 [ms [uoo | 71 [axe [io] ne Jios iso [oz | ns 1465 100%
Il convient de relever que les délibérations du Conseil du Gouvernement portant sur les
nominations aux emplois supérieurs ont concerné essentiellement le poste de Directeur
(78,8%) suivi par le poste de Recteur de faculté avec près de 11,3%.

L'évolution de la répartition des nominations par département au titre de la période 2014-
2024 se présente comme suit :

Essen 46 37 5 4 62 50 33 25 30 39 23 354 [242%
Supérieur

Aménagement du
Territoire National, 13 12 24 3 27 13 15 14 15 22 9 167 | 11,4%
Urbanisme, Habitat
Equipement et Eau 6 6 6 3 17 10 20 10 16 13 9

Agriculture, Pèche
Maritime,
Développement Rural
et Eaux et Forêts

Education Nationale 18 3 20 2 6 6 3 15 5 8 9

Economie et Finances 1 5 6 16 5 1 2 3 14 12 6
Transition Energétique

et Développement 11 12 2 1 6 8 4 3 5 4 10 4,5%
BUEIE

Industrie et Commerce Mi 2 O 14 6 10 2 5 10 S A
Sante et Protection 7 5 3 07 mo EU > 9 5
Sociale

39 23 27 18 64 39 15 22 30 61 35 EAEE
MERE

Il en ressort que le Ministère de l'Enseignement Supérieur, de la Recherche Scientifique et de
l'Innovation, concentre 24,2% des nominations opérées durant cette période, suivi du

Autres

D

RAPPORT SUR LES RESSOURCES HUMAINES

Ministère de l'Aménagement du Territoire National, de l'Urbanisme, de l'Habitat et de la
Politique de la Ville avec un pourcentage de 11,4%, puis du Ministère de l'Equipement et de
l'Eau avec 8%. Le Ministère de l'Agriculture, de la Pêche Maritime, du Développement Rural
et des Eaux et Forêts et le Ministère de l'Éducation Nationale, du Préscolaire et des Sports
accaparent respectivement 6,8% et 6,5% de ces nominations.

Par ailleurs la représentativité de la femme dans ces nominations au titre de la période
précitée et selon le poste occupé est illustrée par le tableau ci-après :

Total des nominations

effectuées entre 2014 et % des Femmes nommées au cours des

Effectif des

femmes nommées 2024 dix dernières années

du total des
Par nominations du total des
Postes 2023 2024 Femmes | Hommes | Total nominations
poste hommes et ON
féminines
femmes

DURS EUE SE 1152 15,7% 12,4% 86,6%
ssimilé
[EREEIEUT 4 2 10 43 53 18,9% 0,7% 4,8%
Général

Président

d'université 0 () 2 29 31 6,5% 0,1% 1,0%
université
Resienr ele 3 1 8 158 166 4,8% 0,5% 3,8%
Faculté

Secrétaire 2 13,1% 0,5% 3,8%
Général

Il ressort de ce tableau ce qui suit :

°e Sur le total des nominations en qualité d'Inspecteur Général, les femmes nommées
à cette fonction représentent 18,9%, et sur l’ensemble des nominations dans les
postes de Directeur et de Secrétaire Général, les nominations féminines
représentent respectivement 15,7% et 13,1% ;

° Sur un total de 209 nominations féminines intervenues au cours de cette période,
86,6% des femmes ont été nommées au poste de Directeur et 4,8% ont été
nommées au poste d’Inspecteur Général et 7,6% ont accédé aux postes de
Secrétaire Général et de Recteur de Faculté avec des parts égales de 3,8% pour
chaque poste;

e Rapporté au nombre total des nominations (hommes et femmes), le poste de
Directeur et Assimilé occupé par les femmes représente 12,4%, suivi du poste
d'Inspecteur Général avec une part de 0,7%, puis des postes de Secrétaire Général
et de Recteur de Faculté avec une part égale de 0,5%.

Le Tableau ci-après présente la répartition par département de la représentativité des
femmes dans les nominations effectuées depuis 2014 jusqu'à Septembre 2024:

AN

PROJET DE LOI DE FINANCES POUR L'ANNEE 2025

Il en ressort ce qui suit :

+ 25,4% des nominations féminines aux emplois supérieurs ont été opérées au niveau
du Ministère de l'Aménagement du Territoire, de l'Urbanisme, de l'Habitat et de la
Politique de la Ville, soit 317% du nombre total des nominations aux postes
supérieurs au sein dudit département ;

e Le Ministère de l'Enseignement Supérieur, de la Recherche Scientifique et de
l'Innovation a bénéficié de 10% des nominations féminines, soit près de 6% des
nominations aux postes supérieurs effectuées au sein de ce département.

e Le troisième rang revient au Ministère de l'Industrie et du Commerce avec 8,6% des
nominations féminines aux emplois supérieurs et une représentativité féminine de
28,6% des nominations supérieures effectuées au sein du département.

Par ailleurs, || convient de préciser que bien que l'accès des femmes aux postes de
responsabilité continue de s'améliorer, il reste encore insuffisant pour assurer une intégration
pleine des femmes en tant qu'acteur clé dans le processus de développement économique et
social de notre pays.

AN

RAPPORT SUR LES RESSOURCES HUMAINES

4.2. Nominations aux postes de responsabilité dans les administrations publiques (chefs de
divisions et chefs de services)

Depuis l'entrée en vigueur du décret n° 2-11-681 du 25 Novembre 2011 fixant les modalités de
nomination des chefs de divisions et chefs de services dans les administrations publiques,
l'accès à ces emplois et à d'autres emplois similaires est soumis à la procédure d'appel à
candidatures ouverte aux candidats remplissant des conditions relatives à l'ancienneté, à la
compétence, au niveau de formation et au mérite.

Au titre de la période allant de l'année 2014 jusqu'à Septembre 2024, les différentes
administrations publiques ont lancé 2.576 appels à la candidature pour pourvoir 10.543
postes de chef de service et assimilé et 3.121 postes de chef de division et assimilé, répartis
comme suit:

Figure 13 : appels à la candidature publiés pour pourvoir les postes de chefs de divisions et chefs de services
dens les administrations publiques au titre de la période 2014-2024

(2024 ZT 185 à

2023 914 6 |

2022 9AA4 320 x Chef de service et

2021 903 218 assimilé
2020 272 Chef de division et
assimilé
2019 836 290
2018 CET 229
2017 764 27
2016 1694 279
2015 1219
(2014 1022 313 »

L'évolution de l'effectif budgétaire du personnel de l'Etat occupant des postes de
responsabilité au cours de la période 2014- 2024 se présente comme suit :

Figure 14 : Effectif occupant les postes de chef de division et de chef de service dans les administrations
publiques au titre de la période 2014-2024

(2024 9:312 3.023 à
2023 9.213 3.016
2022 8.483 2.673
2021 9079 2.8664{ "Chef de
service
2020 8.933 2.871 et
2019 8.906 2.859 assimilé
2018 8.878 2.798
2017 8.721 2.776 u Chef de
division
2016 8608 2.738 et
2015 8.185 2.710 assimilé
2014 7.952 2.548
KL ”

PN

| PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 |

Par ailleurs, la répartition par départements de ces postes de responsabilités de chefs de
divisions et de chefs services au titre de l’année 2023 et jusqu'à Septembre 2024 se présente
comme suit :

Chef de Chef de Chef de Chef de
Départements division et | service et | Total |division et | service et | Total
assimilés | assimilés assimilés | assimilés

Agriculture, Pêche
Maritime, Développement Rural et 208 766 974. 208 766 974.
Eaux et Forêts

Juridictions Financières 205 140 345 205 140 345

Equipement et Eau 180 589 769 168 611 779
Habous et Affaires Islamiques 175 385 560 175 385 560

Economie et Finances 133 434 567 133 434 567

Aménagement du Territoire
National, Urbanisme, Habitat et 126 329 455 126 329 455
Politique de la Ville

Éducation Nationale, Préscolaire et

106 921 1027 106 921 1027
Sports
SEUMESSE, CHINE GE 105 369 474 105 369 474
Communication
Transition Energétique et 86 120 276 86 120 276
Développement Durable
Industrie et Commerce 82 183 265 82 183 265
Affaires Etrangères, Coopération
Africaine et Marocains Résidant à 67 166 233 67 166 233
l'Etranger
Tourisme, Artisanat et Economie 65 253 318 65 253 318
Sociale et Solidaire
Haut-Commissariat au Plan 59 223 282 59 223 282
Conseil National des Droits de 50 34 84 50 34 84
l'Homme
Inclusion Economique, Petite
Entreprise, Emploi et 42 155 197 42 155 197
Compétences
Santé et Protection Sociale 35 113 148 36 114 150
Transport et Logistique 28 164 192 31 172 203

Autres

205 674 879 220 726 946
Total 3.016 9.213 12.229 3.023 9.312 12.335
Il ressort de ce tableau qu'en 2024, sept ministères s’accaparent près de 62% de l’ensemble

des postes de responsabilités de chefs de divisions et chefs de services dans la fonction
publique, et ce comme suit :

AN

RAPPORT SUR LES RESSOURCES HUMAINES

Départements

Intérieur

Éducation Nationale, Préscolaire
et Sports

Agriculture, Pêche

Maritime, Développement Rural et
Eaux et Forêts

Equipement et Eau
Economie et Finances
Habous et Affaires Islamiques

Autres

Total

Répartition du nombre de
postes de responsabilité
par département

30,3%

8,3%
7,9%

6,3%
4,6%
4,5%
38,1%

100%

IL ETAT ACTUEL DES EFFECTIFS DES FONCTIONNAIRES CIVILS DE

L'ETAT

L'analyse de l'effectif budgétaire du personnel civil de l’Etat au titre de l’année 2024, au
niveau de sa structure par échelles, statuts, genre, et tranches d'âge, ainsi qu'au niveau
sectoriel et spatial, révèle une certaine disparité de la répartition des ressources humaines au

sein de la fonction publique.

1. Répartition par départements ministériels

La fonction publique dispose en 2024 d'un effectif de 570.917 fonctionnaires civils dont
environ 90,4% sont concentrés au niveau de 7 départements ministériels :

Fioure 15 : Répertition des effectifs du personnel civil par département en 2024

a

Ministère de l'Education Nationale, du ]
Préscolaire et des Sports

Intérieur

Santé et Protection Sociale
Enseignement Supérieur
Économie et Finances
Justice

Délégation Générale à l'Administration
Pénitentiaire et à la Réinsertion

LU Autres départements

67.496 (11,8%)
28.664 (5,0%)

21.689 (58%)

15.455 (2,7%)

15.108 (2,6%)

54.826 (9,6%)

TN
201.368 (35,3%)

166.311 (29,1%)

/

En effet, le ministère de l'Éducation Nationale, du Préscolaire et des Sports, ainsi que le
ministère de l'Enseignement Supérieur, de la Recherche Scientifique et de l'Innovation,
représentent, à eux seuls, plus de 40,3% de l'effectif budgétaire du personnel civil de l'État.

PN

Ils sont suivis par les départements de l'Intérieur (29,1%), de la Santé et de la Protection
Sociale (11,8%), de l'Économie et des Finances (3,8%), de la Justice (2,7%), et de
l'Administration pénitentiaire (2,6%). Les autres départements ministériels regroupés
emploient 9,6% des fonctionnaires civils.

Par ailleurs, le renforcement du capital humain, en particulier dans le département de
l'Éducation Nationale, fait partie intégrante de la politique d'amélioration de l'offre scolaire et
de l'instauration d’une école publique moderne fondée sur l'équité, l'égalité des chances et la
bonne gouvernance. Dans ce contexte, le Gouvernement à initié un vaste programme de
recrutement au sein des AREFS, atteignant un total de 159.000 enseignants recrutés depuis
l'année scolaire 2016/2017 jusqu'à l’année 2024/2025.

2. Répartition par groupes d’échelles

L'étude de la structure du capital humain par échelles permet d'apprécier le niveau
d'encadrement au sein de l'administration publique, les niveaux de maitrise et d'exécution en
vue d'assurer, dans la mesure du possible, une sorte de complémentarité et d'équilibre entre
ces trois catégories de personnel.

Figure 16 : Structure de l'effectif du personnel civil de l'Etat par groupes d’échelles en 2024
a n

67,6%

Echelles 10 et plus

KL

L'analyse de ce graphique fait ressortir les tendances suivantes :

e Le taux d'encadrement au sein de l’administration publique à nettement progressé,
atteignant 67,6% en 2024, contre 65% en 2014. Cette amélioration résulte
principalement des avancements de grade et des opérations ciblées de recrutement
récentes qui ont été orientées vers les cadres ;

° Les effectifs du personnel de maîtrise (échelles 7 à 9) et du personnel d'exécution
(échelle 6 et assimilés) représentent en 2024 respectivement 20% et 12,4% de l'effectif
budgétaire du personnel civil de l'Etat.

3. Répartition par statuts

Les statuts régissant le personnel civil de l'Etat ont fait l’objet d’une action d'harmonisation
et de fusion en vue d'optimiser et de rationaliser la gestion des ressources humaines dans
l'administration publique à travers l’uniformisation des procédures et la réduction du nombre
de statuts. Ainsi, le personnel de l’Etat est régi à travers trois grandes catégories de statuts à
savoir : les statuts interministériels, les statuts particuliers et les statuts spéciaux.

Le graphique ci-après donne la proportion de chacune des catégories sus-indiqués :

AN

RAPPORT SUR LES RESSOURCES HUMAINES

Figure 17 : Structure de l'effectif du personnel civil de FEtat par type de statuts

[ D
Statuts spéciaux Autres
3% / 0,4%
Statuts
interministériels
25,4%

Statuts particuliers
71,2%

Ne J

3.1, Statuts interministériels

Avec une proportion d'environ 25,4% de l'effectif total du personnel civil de l'État, le
personnel interministériel est composé des corps d'administrateurs, d'ingénieurs, de
techniciens, de rédacteurs, d'adjoints administratifs et d'adjoints techniques, ainsi que de
médecins, d'infirmiers et de techniciens de la santé.

La structure, par corps, de ce personnel dont l'effectif s'élève à 145.022 se présente comme
suit :

Figure 18 : Structure de l'effectif du personnel civil de l'Etat relevant du personnel interministériel
[ Autres Adjoints à
10,6% administratifs et

N TT techniques

14,6%

Infirmiers
24,3%

verte

RIDIZZILZ

Marre
4

+ sn
Techniciens et

Le
LL" &.
Médecins .
10,3% . rédacteurs
Ingénieurs 15%

7,1%
Ne J

Il ressort de ce graphique que :

e Le corps des infirmiers et techniciens de la santé constitue la majorité du personnel
interministériel avec un effectif de 35.297, soit un taux de 24,3%, suivi des
administrateurs, des techniciens et rédacteurs et des adjoints techniques et
administratifs avec des effectifs respectifs de 26.196, 21.583 et 21.179 , soit des parts
respectives de 18,1%, 15% et 14,6%. ;

+ Les médecins et les ingénieurs dont les effectifs s'élèvent respectivement à 14.953 et
de 10.316 représentent des parts respectives de 10,3% et 7,1% du corps interministériel

dans la fonction publique.

3.2. Statuts particuliers

L'effectif du personnel régi par les statuts particuliers représente 71,2% du total du personnel
civil. Il s'agit essentiellement du personnel de l'Education Nationale, du personnel de sécurité
(DGSN et Protection Civile), du Secrétariat Greffe, des Enseignants Chercheurs, de
l'Economie et des Finances, de l'Administration Pénitentiaires et autres.

L'analyse de la composition de cette catégorie de fonctionnaires régie par des statuts
particuliers révèle que les fonctionnaires relevant du statut particulier du personnel de
l'Education Nationale représentent une proportion de 49,1%, suivi du personnel de sécurité
avec un taux de 29,7%.

Figure 19 : Structure de l'effectif du personnel civil de l'Etat relevant des statuts particuliers

4 . inictrat à
Enseignants Secrétariat greffe Administration
chercheurs 3,8% Pénitentiaire
4,7% / La 3,6%
Economie et \ Autres
Finances INK | IT ZI4
L À . DGSN et protection
À civile
29,7%
Education Nationale
49,1%
L J
3.3. Statuts spéciaux

Les statuts spéciaux régissent les corps des magistrats de l’ordre judiciaire, des magistrats
des juridictions financières, des administrateurs de l'Intérieur, des agents d'autorité et les
fonctionnaires des deux chambres du Parlement. Le personnel y assujetti s'élève à 17.604
représentant ainsi 3% du personnel civil global de l'Etat.

4. Répartition par tranches d'âge

L'analyse de la pyramide des âges du personnel de l'État constitue un indicateur essentiel
pour la gestion prévisionnelle des emplois et des compétences (GEPEC). Cet instrument
moderne de gestion et d'optimisation des ressources humaines offre, d'une part, une
visibilité sur les départs à la retraite et, d'autre part, permet la mise en œuvre de
programmes appropriés en matière de formation et de recrutement, et Ainsi, il facilite la
préparation de la relève et répond de manière proactive aux besoins des administrations en

matière de ressources humaines.

La structure des effectifs du personnel civil par tranches d'âge, au titre de l'année 2024 se
présente comme suit :

AN

RAPPORT SUR LES RESSOURCES HUMAINES

Figure 20 : Structure des effectifs du personnel civil par tranches d'âge

F

22,01%

14,75% .
102 13,69%
12,19% 6 12,80%
7,79% , L)
2,15% 7) L/) 7
11), # 1 j À F , / ==
<25 ans 25 à moins 30 à moins 35 à moins 40 à moins 45 à moins 50 à moins 55 ans et

de 30 ans de 35 ans de 40 ans de 45 ans de 50 ans de 55 ans plus

Le ”

° Les jeunes fonctionnaires âgés de moins de 35 ans représentent près de 22% de
l'effectif global des fonctionnaires civils de l'État ;

° Les fonctionnaires appartenant à la tranche d'âge de 35 à 49 ans constituent 43% des
effectifs, tandis que ceux âgés de 50 ans et plus représentent environ 35% de
l'ensemble des fonctionnaires civils de l'État.

Par ailleurs, la structure des effectifs du personnel civil par départements et par tranches
d'âge, diffère d’un département à un autre et ce, commeillustré dans le tableau suivant :

Santé et | Economie
Protection et
Sociale Finances

Education | Enseignement
Nationale Supérieur

Tranches d’âge

< 25 ans

0,0%

1,0%

2,0%

10,6%

1,9%

1,1%

25 à moins de 30 ans 0,3% 3,8% 14,6% 18,4% 10,3% 6,2%
30 à moins de 35 ans 7,0% 9,0% 18,0% 17,5% 16,9% 9,0%
35 à moins de 40 ans 15,2% 11,9% 15,7% 14,7% 14,8% 13,4%
40 à moins de 45 ans 18,5% 1,5% 13,1% 10,9% 9,0% 15,4%
45 à moins de 50 ans 20,0% 12,1% 9,6% 5,8% 9,6% 16,0%
50 à moins de 55 ans 15,1% 14,3% 10,8% 7,7% 13,8% 15,6%
55 ans et plus 23,9% 36,4% 16,2% 14,4% 23,7% 23,3%

Total 100% 100% 100% 100% 100% 100%

5. Départs à la retraite prévus pour la période 2024-2028

D'après les prévisions de la Caisse Marocaine des Retraites, 65.213 fonctionnaires devraient
partir à la retraite pour limite d'âge au cours de la période 2024-2028, soit 13% de l'effectif
actuel du personnel civil de l'Etat. Ces départs sont illustrés par le tableau ci-après :

PSN

PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 |

% par
Total rapport au |% rapporté à
Administrations total des l'effectif du
2024-2028 ñ 2
départs pour | département
limite d'âge

Education 5.675 3.021 6.485 6.013 5.717 26.91 41,3% 13,7%
Nationale

1.798 2.761 2986 3.257 3.260 14.062 21,6% 12,2%
796 1435 1233 1176 1078 5.718 8,8% 9,6%

711 984 974 1.020 968 4.657 71% 18,3%
Supérieur

160 376 440 464 450 1.890 2,9% 12,5%

160 390 367 418 384 1.719 2,6% 9,4%
Finances

1.184 2.191 2.237 2.306 2.338 10.256 15,7% 14,9%
D ras roues (rss [arse(issé (use ss [icon [css

6. Répartition par genre

La participation de la femme à l'effort de développement économique et social est un
indicateur de base pour l'évaluation du degré d'intégration de l'approche genre dans les
politiques publiques et les programmes Gouvernementaux. Le Maroc a naturellement fait de
ce chantier un choix irréversible et a confirmé cet engagement en souscrivant aux principes
et obligations énoncés dans les conventions internationales sur les droits de l'Homme qui
soulignent que les droits et les libertés ne doivent nullement être assujettis à des distinctions
de quelque nature que ce soit. Le Maroc a fait également preuve de cet engagement en
ratifiant bon nombre d'instruments de droits de l'Homme notamment la Convention sur
l'élimination de toutes les formes de discrimination à l'égard des femmes.

Au niveau national, la constitution de 2011 a institué le principe d'égalité entre l’homme et la
femme notamment dans son article 19 qui énonce que «l'Etat œuvre à la parité entre les
hommes et les femmes...» et en annonçant la mise en place d'une autorité pour la parité et la
lutte contre toutes les formes de discrimination. Autre pierre à l'édifice de la consolidation
des droits de la femme réside dans le lancement du programme national intégré
d'autonomisation économique et social des femmes à l'horizon 2030 en partenariat avec les
Nations Unies.

Dans la même visée, le Maroc s'active à donner à l'approche genre une assise clairement
définie dans ses choix budgétaires et ce, via la Budgétisation Sensible au Genre.

Il n’en demeure pas moins qu’en dépit de ces avancées couplées aux stratégies menées par
le Gouvernement, avec l'appui des instances de l'ONU, le niveau d'intégration des femmes
dans le marché du travail n'est pas encore à la hauteur des aspirations en termes de taux de
représentativité féminine et de taux d'accès aux postes de décision.

Le taux actuel de féminisation dans l’administration publique est de 36,3%, contre 63,7%
pour les hommes, comme indiqué dans le graphe ci-après :

AN

RAPPORT SUR LES RESSOURCES HUMAINES

Figure 21 : Structure des effectifs du personnel civil par genre

CL Femmes Hommes

L'effectif des femmes par départements se présente comme suit :

% Féminin par

% Féminin par n :
, . rapport à l'effectif
Département PER à! Elus global des femmes
civil de la fonction delaf :
publique e la onction
publique

Economie et Finances 1,5%

44,5%
22,0%
8,3%
5,2%
4,2%
4,1%
11,7%

TOTAL 36,3% 100,0%

Il ressort de ce tableau que trois départements à envergure sociale, en l'occurrence
l'Education Nationale, la Santé et l'Enseignement Supérieur, emploient près de 72% de
l'effectif féminin de la Fonction Publique avec des parts respectives de 44,5%, 22% et

5,2%.

La répartition des effectifs des femmes fonctionnaires au sein de chaque département est
donnée par le tableau suivant :

Département

Santé et Protection Sociale
Développement Durable

Transition Numérique et Réforme de l'Administration

Investissement, Convergence et Evaluation des Politiques
Publiques

% Féminin par rapport à
l'effectif civil total du
personnel du département

67,1%

53,5%
51,9%

51,5%

PEN

49,5%
49,3%
48,7%
48,5%
47,9%
46,2%
45,7%
45,6%
45,2%
43,9%
431%
42,0%
42,0%
417%
41,0%
4,0%
40,8%
40,1%
39,0%
35,8%
35,7%
34,0%
H.C. Aux Anciens Résistants.et Anciens Membres de l'Armée de
Libération 51,5%
30,3%
Conseil Supérieur du Pouvoir Judiciaire 28,9%
Pêche Maritime 28,7%
Sport 27,0%
Cour Royale 21,5%
Intérieur 13,8%
Délégation Générale à l'Administration Pénitentiaire et à la
Réinsertion IHSERS
Protection Civile 4,1%

L'analyse de ce tableau révèle une représentativité féminine assez remarquable au niveau
d'un certain nombre de départements avec des taux qui varient entre 40% (Agriculture et
Développement Rural) et 671% (Santé et Protection Sociale). Cependant cette

AN

RAPPORT SUR LES RESSOURCES HUMAINES

représentativité se situe aux alentours d’une moyenne de 28% de l'effectif du personnel civil
de chacun des autres départements.

7. Répartition par régions

Le Gouvernement accorde une attention particulière à la mise en œuvre du processus de
déconcentration administrative en vue d'apporter l'appui nécessaire à la réussite de la
régionalisation avancée, adoptée par le Maroc pour l'exécution des programmes de

développement et la mise en œuvre des stratégies sectorielles au niveau territorial.

Ce processus est conditionné par l’adoption d’un nouveau mode de gouvernance territoriale
en transférant certains pouvoirs et missions de l'administration centrale aux services
déconcentrés.

La mise en œuvre de ce chantier d'envergure nécessite la mobilisation aux services
déconcentrés de l'Etat des ressources humaines et matérielles nécessaires pour leur
fonctionnement tout en leur conférant les pouvoirs nécessaires pour accomplir leurs
missions au niveau territorial.

Or, la répartition actuelle des fonctionnaires civils de l'Etat par région fait ressortir certaines
disparités, entre régions, en matière de ressources humaines. En effet, et comme illustré dans
le tableau ci-dessous, près de 70% du personnel civil de l'Etat se concentre au niveau de cinq
régions à savoir : Rabat-Salé-Kénitra, Casablanca-Settat, Fès-Meknès, Marrakech-Safi et
Tanger-Tétouan-Al Hoceima, les 7 autres régions du Royaume bénéficient de près de 30%
de l’ensemble de ces fonctionnaires.

Part en %

Région

Rabat-Salé-Kénitra 23,7%

Casablanca-Settat 14,0%

Fès-Meknès 12,0%
Marrakech-Safi 10,7%

Tanger-Tétouan-Al Hoceima 9,2%
Souss-Massa 7,5%

Oriental 6,6%
Béni Mellal-Khénifra 5,9%
Darâa-Tafilalet 4,9%
Laâyoune-Sakia El Hamra 2,7%
Guelmim-Oued Noun 1,9%

Dakhla-Oued Eddahab 0,9%

Total 100%

PSN

| PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 | D
3EME PARTIE : DEPENSES DE PERSONNEL

Les dépenses de personnel constituent une composante importante dans la structure des
dépenses publiques au vu des masses financières conséquentes qu'elles mobilisent, et
suscitent de ce fait, un intérêt particulier de la part du Gouvernement en matière de
programmation budgétaire, de budgétisation, de rationalisation et de contrôle. En effet, La
maîtrise de l’évolution de ces dépenses constitue un enjeu primordial pour le Gouvernement
et obéit au défi de mise en cohérence de l'obligation de doter l'administration de moyens
humains nécessaires au bon fonctionnement des services publics et des besoins pressants
de renforcer les choix affichés de réallocation des crédits budgétaires au profit du budget
d'investissement.

| EVOLUTION DES DEPENSES DE PERSONNEL AU COURS DE LA
PERIODE 2014-2024

Les dépenses de personnel de l'Etat sont passées de 115,42 MMD en 2014 à 161,62 MMD en
2024, soit, une évolution globale de près de 40% et une évolution moyenne annuelle de
3,42%.

Figure 22 : Evolution des dépenses de personnel - En Millions de Dirhams -

| D
161.623
155.794
147.755 _—
153530 40456 =
no27s 121186 127-719 D _
15.424 16.856 118.704 Î8. se
a = 1 —, Æ
Ua ' | | : T T _ Tr =
2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024

Deux phases peuvent être distinguées au cours de ces dix dernières années :

2014-2018 : Une décélération de la croissance des dépenses de personnel à été
observée durant cette période, avec un taux de progression stabilisé autour d'une
moyenne annuelle de 1,23 %. Cette tendance s'explique en partie par l'effet conjugué
des suppressions de postes budgétaires suite aux départs à la retraite et des mesures
gouvernementales visant à maîtriser l'évolution des dépenses de personnel.

2018-2024 : Une augmentation notable des dépenses de personnel, atteignant en
moyenne +4,92% par an, découle principalement de la mise en œuvre des décisions
relatives aux révisions salariales prises durant cette période dans le cadre du dialogue
social au profit du personnel de l'État.

PN

RAPPORT SUR LES RESSOURCES HUMAINES

Indicateurs des dépenses de personnel

PIB en ee se Evolution des | Dépenses de EEE FETE
Millions de P Millions dépenses de personnel ersonnel ersonnel
DH de DH personnel /PIB P /8G P /8F

2014 1.001.454 115.424 - 11,53% 37,52% 59,26%
2015 1.078.119 116.856 1,24% 10,84% 38,54% 64,49%
2016 1.094.249 118.704 1,58% 10,85% 38,05% 62,75%
2017 1.148.895 119.278 0,48% 10,38% 36,15% 62,26%
2018 1.195.237 121.186 1,60% 10,14% 37,01% 61,34%
2019 1.239.836 127.719 5,39% 10,30% 34,93% 59,23%
2020 1.152.477 133.530 4,55% 1,59% 33,15% 61,97%
2021 1.276.563 140.456 5,19% 1,00% 35,99% 61,10%
2022 1.330.558 147.755 5,20% 110% 31,95% 52,99%
2023 1.463.358 155.794 5,44% 10,65% 32,03% 57,46%
2024 1.542.804 161.623 3,74% 10,48% 32,44% 57,84%

1. Ratio des dépenses de personnel par rapport au Produit Intérieur Brut (PIB)

La proportion annuelle moyenne des dépenses de personnel par rapport au Produit Intérieur
Brut sur les dix dernières années s'est établie à 10,80%. Cet indicateur a connu une
régression au cours de la période 2014-2019, pour ensuite se relancer en 2020 à raison de
1,59% et puis prendre une trajectoire baissière pour se stabiliser aux alentours d'une

moyenne annuelle de 10,81% pendant la période 2021-2024.

Figure 23 : Evolution des dépenses de personnel par rapport au PIB
a TN

11,53% 11,59%

10,47%

10,84% 10,14%

10,38% 10,30%

2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024

Le pic enregistré par ce ratio en 2020 est expliqué en grande partie par les retombées
économiques de la pandémie du Covid-19 sur l’économie nationale durant l’année 2020 qui a

été marquée par une régression du PIB par rapport à l’année 2019.

2. Ratio des dépenses de personnel par rapport au Budget Général (BG)

AU titre de la période 2014-2024, les dépenses de personnel représentent une proportion
moyenne de 35,25% des dépenses du budget général. A noter que ce ratio a enregistré un
taux de 32,44% en 2024.

Figure 24 : Structure des dépenses du Budget Général -Année 2024-
[ n

Dépenses de personnel

= Dette publique

« Dépenses d'investissement du budget

général

“ Dépenses materiels et dépenses diverses

m Charges communes

+Dépenses de compensation

* Dépenses relatives au remboursements
degrevements et restitutions fiscaux

Dépenses imprévues et dotations
provisionnelles

Ne J
Figure 25 : Evolution des dépenses de personnel par rapport aux dépenses du Budget Général
4 D

37,52% 38,05%
37,01%

32,03%

LC 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024

/

3. Ratio des dépenses de personnel par rapport au Budget de Fonctionnement

Cet indicateur s'est stabilisé autour d’un taux annuel moyen de 60,06%. L'évolution annuelle
de ce ratio est retracée par le graphique suivant :

PN

RAPPORT SUR LES RESSOURCES HUMAINES

Figure 26 : Evolution des dépenses de personnel par rapport au Budget de Fonctionnement

4 »

62,26%

57,84%

2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024
/

4. Ratio des dépenses de personnel par rapport aux Recettes Ordinaires

La part des recettes ordinaires affectées aux dépenses de personnel à enregistré durant la
période 2014-2024 une moyenne annuelle de 52%, un taux qui reste élevé et ce au détriment
d'une affectation conséquente de moyens aux dépenses d'investissement.

IL DÉPENSES DE PERSONNEL DE L'ETAT AU TITRE DE L’ANNEE 2024
1. Dépenses de personnel civil par départements

Près de 88% des dépenses de personnel civil de l'Etat sont concentrées au niveau de sept
départements, à savoir celui de l'Education Nationale, du Préscolaire et des Sports avec
37,12%, suivi de l'Intérieur avec 21,15%, des Ministères de la Santé et de la Protection Sociale,
de l'Enseignement Supérieur, de la Recherche Scientifique et de l'Innovation, de l'Economie
et des Finances, de la Justice, des Affaires Etrangères, de la Coopération Africaine et des
Marocains Résidant à l'Etranger avec respectivement 12,81, 8,21%, 3.57%, 2,83% et 2,46%. Les

autres départements absorbent 11,85% des crédits de personnel.

La concentration des dépenses de personnel et des effectifs dans certains départements
(Education Nationale, Intérieur, Santé et Protection Sociale .) est due à la nature et à la
sensibilité des missions incompressibles assignées à ces départements.

Dépenses de personnel au titre de

. . %
la loi de finances 2024 en MDH

Département

Ministère de l'Education Nationale, du 37,12%
Préscolaire et des Sports

Ministère de l'Intérieur 23.851 21,15%
Ministère de la Santé et de la Protection Sociale 14.450 12,81%
Ministère de l'Enseignement Supérieur, de la o

Recherche Scientifique et de l'Innovation 2262 SAS
Ministère de l'Economie et des Finances 4.020 3,57%

PN

Ministère de la Justice 3.193 2,83%

Ministère des Affaires Etrangères, de la
Coopération Africaine et des Marocains Résidant 2.769 2,46%
à l'Etranger

Conseil Supérieur du Pouvoir Judicaire 2.698 2,39%

Délégation Générale à | Administration 1975 175%
Pénitentiaire et à la Réinsertion

Ministère des Habous et des Affaires Islamiques 1.189 1,06%
Ministère de l'Equipement et de l'Eau 1.016 0,90%

Autres départements 6.481 5,75%

2. Dépenses de personnel civil par régions

La structure des dépenses de personnel par régions est illustrée à travers le graphique
suivant :

Figure 27 : Répartition des dépenses de personnel par régions

f Laâyoune-Sakia El Guelmim-Oued D
Hamra Noun Dakhla-Oued Ed-

3% 1,9% DS roue

Daréa-Tafilalet 1,1%
ATK

Beni Mellal-Khénifra
5,5%

Rabat-Salé-Kénitra

22,4%

Oriental
5,7%

Souss-Massa
6,8%

Casablanca-Settat
16,3%

Marrakech-Safi
9,5%

Fès-Meknès
1,7%

Tanger-Tétouan-Al
Hoceima

e 11,4% )

Il en ressort ce qui suit :

+ 78,14% des dépenses de personnel sont concentrées au niveau de 6 régions : Rabat-
Salé-Kenitra, Casablanca-Settat, Fès-Meknès, Tanger-Tétouan-Al Hoceima, Marrakech-
Safi et Souss-Massa;

AN

RAPPORT SUR LES RESSOURCES HUMAINES

e Le personnel civil de l'Etat relevant des administrations situées au niveau de la région
de Rabat-Salé-Kenitra bénéficie de 22,4% des dépenses de personnel. Cette part
importante est due essentiellement au regroupement des administrations centrales
dans la ville de Rabat.

Par ailleurs, force est de constater l'absence de corrélation entre la répartition des dépenses
de personnel par régions et la contribution à la croissance du pays. En effet :

Au niveau de la région de Casablanca-Settat, premier pôle économique, où la
part au PIB est la plus élevée (31,43%) et qui compte une population importante,
les dépenses de personnel ne représentent que 16,3%.

Les quatre régions de Casablanca-Settat, Fès-Meknès, Tanger-Tétouan-Al
Hoceima et Marrakech-Safi contribuent à hauteur de 58,16% dans la production
de la richesse nationale, et s'accaparent 48,9% des dépenses de personnel alors
que les huit autres régions absorbent 511% de ces dépenses et contribuent à
hauteur de 41,48% au produit intérieur brut.

Contribution régionale à la
Régions création du Produit

Intérieur Brut en valeur

Casablanca - Settat 31,43%
Rabat - Salé - Kénitra 16,10%
Tanger - Tétouan - Al Hoceima 10,46%
Marrakech - Safi 8,31%
Fès - Meknès 7,96%
Souss - Massa 6,59%
Béni Mellal - Khénifra 6,15%
Oriental 5,15%
Drêa - Tafilalet 2,96%
Lâêayoune - Sakia El Hamra 2,21%
Guelmim - Oued Noun 1,50%

Dakhla - Oued Ed Dahab 1,18%

TOTAL 100%

3. Dépenses de personnel civil par échelles

La structure des dépenses de personnel civil au titre de l'année 2024 par groupes d’'échelles
se présente comme suit :

+ Le personnel classé à l’échelle 6 et assimilés qui représente 12,4% de l'effectif civil
global, bénéficie de 7,32% des dépenses de personnel, génère 0,53% de l'impôt sur le

revenu et participe à hauteur de 7,47% aux cotisations de retraite ;

+ Les fonctionnaires classés aux échelles 7 à 9 qui représentent 20% de l'effectif total,
bénéficient de 10,58% des dépenses affectées, contribuent à hauteur de 1,19% des
recettes de l'impôt sur le revenu et versent 10,26% au titre des cotisations de retraite ;

+ La catégorie de personnel classée à l'échelle 10 et plus qui représente 67,6% de
l'effectif civil global, absorbe 82,10% des dépenses de personnel, contribue à 98,28%

au titre de l'impôt sur le revenu et verse 82,27% des cotisations au titre de la retraite.

Figure 28 : Répartition des dépenses de personnel civil par échelles

[ Echelle 6 et \
assimilés Echelles 7 à 9
7,32% 10,58%

Echelles 10 et plus
82,10%

KL /

4. Niveaux des salaires dans la fonction publique au titre de Fannée 2024
4.1. Salaire mensuel net moyen dans la fonction publique

Sous l'effet conjugué de la promotion de grade et des augmentations salariales décidées par
le Gouvernement au profit des fonctionnaires dans le cadre du dialogue social, une nette
amélioration du salaire mensuel net moyen servi dans la fonction publique a été constatée
au cours des 10 dernières années (2014-2024). En effet, ce salaire est passé de 7.300 DH en
2014 à 9.500 DH en 2024, enregistrant ainsi une augmentation globale de 30,14% au titre de
cette période, soit une augmentation annuelle moyenne de 2,67%.

4.2. Salaire mensuel net moyen par groupes d’échelles

La structure du salaire mensuel net moyen par groupes d’échelles se présente en 2024
comme suit :

Figure 29 : Salaire mensuel net moyen par groupes d'échelles

4 »

1.178

12.000
10.000
8.000
6.000
4.000
2.000

Echelle 6 et Echelles 7 à 9 Echelles 10 et +
assimilés

RAPPORT SUR LES RESSOURCES HUMAINES

- Personnel d'exécution classé à l’échelle 6 et assimilés : 5.203 DH ;
- Personnel de maitrise classé aux échelles 7 à 9 : 6.512 DH ;
-_ Cadres et cadres supérieurs (échelles 10 et plus) : 11.178 DH.

4.3. Répartition des fonctionnaires civils de PEtat par tranches de salaires
Cette répartition présente les principales caractéristiques suivantes :

+ 3,93% des fonctionnaires civils de l'Etat perçoivent une rémunération mensuelle nette
comprise entre 4000 DH (salaire minimum) et 4.500 DH ;

e 15,24% des fonctionnaires bénéficient d'un salaire mensuel net inférieur où égal à
6.000 DH ;

e 70,19% des fonctionnaires civils de l'Etat perçoivent des salaires mensuels nets entre
6.000 DH et 14.000 DH ;

e _3,57% des fonctionnaires ont des salaires nets dépassant 20.000 DH par mois.

Répartition des effectifs par tranches de salaires

Tranches de salaire mensuel net (DH) %

4.000-4.500 3,93% 3,93%

4.500-6.000 11,31% 15,24%

6.000-8.000 30,93% 46,17%
8.000-10.000 19,54% 65,71%
10.000-12.000 14,91% 80,62%
12.000-14.000 4,81% 85,43%
14.000-16.000 6,86% 92,29%
16.000-18.000 2,78% 95,07%
18.000-20.000 1,36% 96,43%
20.000-25.000 196% 98,39%
25.000-30.000 0,98% 99,37%
30.000-40.000 0,51% 99,88%

40.000 et + 0,12% 100,00%

4.4. Salaire minimum

Le salaire minimum dans là fonction publique à connu au cours de ces dernières années des
révisions importantes en passant de 3.000 DH en 2014 à 3.258 DH en 2020 pour atteindre
3.500 DH en 2023, 4.000 DH en 2024 et 4.500 DH en 2025, et ce suite aux décisions prises

par le Gouvernement dans le cadre des différentes sessions du dialogue social.

Il. EXECUTION DES DEPENSES DE PERSONNEL

1. Exécution des dépenses de personnel au titre de l’année 2023

Avec un taux de réalisation de 97,41% par rapport aux prévisions de la Loi de Finances 2023,
les dépenses de personnel réellement servies au titre de l'année 2023 se sont stabilisées aux
alentours de 151,765 MMDH (128,147 MMDH payés par la Direction des Dépenses de
Personnel (DDP) et 23,618MMDH payés par les comptables des réseaux de la TGR) contre
147,756 MMDH en 2022.

L'analyse des dépenses réelles au titre de l’année 2023 par département et par type
d'opérations permet de dégager les conclusions suivantes :

1.1. Exécution des dépenses de personnel par département

Les dépenses de personnel par département réellement servies en 2023 par la Direction des
Dépenses de Personnel (DDP) se présentent comme suit :

Départements Année 2023 Part dans les dépenses
: - en millions de DH - de personnel en %
Ministère de l'Education Nationale, Préscolaire et
, - .. 40.691 31,75%
Sports et Secteur de l'Enseignement Supérieur

Ministère de l'Intérieur 25.711 20,06%

Ministère de la Santé et de la Protection Sociale 13.017 10,16%

Ministère de l'Enseignement Supérieur, de la 0
Recherche Scientifique et de l'Innovation SE SAÈRS

Ministère de la Justice 3.054 2,38%

Ministère de l'Economie et des Finances 3.121 2,44%

Autres départements 34.238 26,72%

Il en ressort que 73,28% des dépenses de personnel réellement exécutées en 2023
concernent 6 ministères et ce, comme indiqué dans le tableau ci-dessus.

1.2. Régularisations des recrutements, des avancements de grade et d’échelon

Les régularisations effectuées au titre des avancements de grade et d’échelon en 2023 ont
atteint respectivement 4.631MDH et 2.089MDH, ce qui représente environ 54,86% et 24,74%
du montant global des régularisations qui a atteint une enveloppe de 8.442MDH, soit 6,59%
de l’ensemble des dépenses de personnel servies en 2023.

1.3. Composante des retenues réglementaires

Au titre de l’année 2023, les retenues réglementaires au titre de l’Impôt sur le revenu et au
titre des cotisations sociales ont atteint 44.978MDH, soit respectivement 9.936MDH et

35.042MDH et représentent 35,10% des dépenses de personnel.

D

RAPPORT SUR LES RESSOURCES HUMAINES

Part dans les dépenses
de personnel servies par

Année 2023

Retenues réglementaires - en millions de DH -

la DDP en %

Impôt sur le revenu (IR) 9.936 7,75%
Caisse marocaine des retraites (CMR) 28.759 22,44%
Régime collectif d'allocation de retraite (RCAR) 175 0,14%
Assurance maladie obligatoire 3.647 2,85%
Mutuelles 2.075 1,62%
Autres retenues 386 0,30%

TOTAL 44.978 LEALE

2. Exécution des dépenses de personnel au titre de l’année 2024 (du 1er Janvier au 31
Août 2024)

L'exécution des dépenses de personnel au titre des 8 premiers mois de l'année 2024 s'est
établie à 106,53 milliards de dirhams, soit un taux de réalisation de 65,91% par rapport aux
prévisions des dépenses de personnel au titre de l’année 2024.


"""
    conversation_history = StreamlitChatMessageHistory()  # Créez l'instance pour l'historique

    st.header("PLF2025: Explorez le rapport sur les ressources humaines à travers notre chatbot 💬")
    
    # Load the document
    #docx = 'PLF2025-Rapport-FoncierPublic_Fr.docx'
    
    #if docx is not None:
        # Lire le texte du document
        #text = docx2txt.process(docx)
        #with open("so.txt", "w", encoding="utf-8") as fichier:
            #fichier.write(text)

        # Afficher toujours la barre de saisie
    st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)
    selected_questions = st.sidebar.radio("****Choisir :****", questions)
        # Afficher toujours la barre de saisie
    query_input = st.text_input("", key="text_input_query", placeholder="Posez votre question ici...", help="Posez votre question ici...")
    st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)

    if query_input and query_input not in st.session_state.previous_question:
        query = query_input
        st.session_state.previous_question.append(query_input)
    elif selected_questions:
        query = selected_questions
    else:
        query = ""

    if query :
        st.session_state.conversation_history.add_user_message(query) 
        if "Donnez-moi un résumé du rapport" in query:
            summary="""Le rapport sur les ressources humaines du Projet de Loi de Finances pour l'année 2025 met en avant les principales orientations et objectifs liés à la gestion des effectifs publics. Il présente une vue d'ensemble des postes à pourvoir, des concours organisés, et des appels à candidatures pour des postes d'experts. Le document souligne l'importance de l'optimisation des ressources humaines dans l'administration publique, visant une meilleure gestion des compétences et des besoins en personnel, en cohérence avec les priorités budgétaires du gouvernement. Les concours et appels à candidature sont encadrés pour assurer une transparence et une efficacité dans le recrutement."""
            st.session_state.conversation_history.add_ai_message(summary) 

        else:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"{query}. Répondre à la question d'apeés ce texte repondre justement à partir de texte ne donne pas des autre information voila le texte: {text} "
                    )
                }
            ]

            # Appeler l'API OpenAI pour obtenir le résumé
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )

            # Récupérer le contenu de la réponse

            summary = response['choices'][0]['message']['content']
           
                # Votre logique pour traiter les réponses
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(response)
            st.session_state.conversation_history.add_ai_message(summary)  # Ajouter à l'historique
            
            # Afficher la question et le résumé de l'assistant
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(summary)

            # Format et afficher les messages comme précédemment
                
            # Format et afficher les messages comme précédemment
        formatted_messages = []
        previous_role = None 
        if st.session_state.conversation_history.messages: # Variable pour stocker le rôle du message précédent
                for msg in conversation_history.messages:
                    role = "user" if msg.type == "human" else "assistant"
                    avatar = "🧑" if role == "user" else "🤖"
                    css_class = "user-message" if role == "user" else "assistant-message"

                    if role == "user" and previous_role == "assistant":
                        message_div = f'<div class="{css_class}" style="margin-top: 25px;">{msg.content}</div>'
                    else:
                        message_div = f'<div class="{css_class}">{msg.content}</div>'

                    avatar_div = f'<div class="avatar">{avatar}</div>'
                
                    if role == "user":
                        formatted_message = f'<div class="message-container user"><div class="message-avatar">{avatar_div}</div><div class="message-content">{message_div}</div></div>'
                    else:
                        formatted_message = f'<div class="message-container assistant"><div class="message-content">{message_div}</div><div class="message-avatar">{avatar_div}</div></div>'
                
                    formatted_messages.append(formatted_message)
                    previous_role = role  # Mettre à jour le rôle du message précédent

                messages_html = "\n".join(formatted_messages)
                st.markdown(messages_html, unsafe_allow_html=True)
if __name__ == '__main__':
    main()
