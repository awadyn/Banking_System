module Navigation exposing (..)


import Html exposing (..)
import Html.Attributes exposing (..)
import Http exposing (..)


type Base a = Some a | None


base_url: String
base_url = "http://localhost:5000/"

navigation_bar: Html msg
navigation_bar =
  nav[]
    [ text " | "
    , a [ href (base_url ++ "register"), style [("text-decoration", "none")]] [ text "Register"]
    , text " | "
    , a [ href (base_url ++ "balance"), style [("text-decoration", "none")]] [ text "Balance" ]
    , text " | "
    , a [ href (base_url ++ "transfers"), style [("text-decoration", "none")]] [ text "Transfers" ]
    , text " | "
    , a [ href (base_url ++ "create_transfer"), style [("text-decoration", "none")]] [ text "Create Transfer" ]
    , text " | "
    , a [ href (base_url ++ "handle_incoming_request"), style [("text-decoration", "none")]] [ text "Handle Incoming Transfer" ]
    , text " | "
    ]

