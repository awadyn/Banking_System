module Handle_Transfer exposing (..)

import Html exposing (..)
import Html.App as App
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http exposing (..)
import Task exposing (Task)
import String exposing (..) 
import Json.Decode as Decode exposing (..)
import Json.Encode as Encode exposing (..)

import Navigation exposing (..)

main = App.program { init = init, view = view, update = update, subscriptions = subscriptions }


-- MODEL
type alias Model = { userid : String, password : String, transferid : String, approve : Bool, message: String }


-- INIT
init: (Model, Cmd Msg)
init = (Model "" "" "" False "", Cmd.none)


-- UPDATE
handle_incoming_request_url: String
handle_incoming_request_url = "http://localhost:5000/handle_incoming_request"


handleRequestEncoder: Model -> Encode.Value
handleRequestEncoder model =
  Encode.object [("userid", Encode.string model.userid), ("password", Encode.string model.password), ("transferid", Encode.string model.transferid), ("approve", Encode.bool model.approve)]


handleRequestDecoder: Decoder (String, String, String)
handleRequestDecoder =
  Decode.object3 (,,)
    ("Request Status" := Decode.string)
    ("Current Balance" := Decode.string)
    ("Error" := Decode.string)


handleRequest: Model -> String -> Task Http.Error (String, String, String)
handleRequest model api_url =
  {
    verb = "POST"
  , headers = [("Content-Type", "application/json")]
  , url = api_url
  , body = Http.string <| Encode.encode 0 <| handleRequestEncoder model
  }
  |> Http.send Http.defaultSettings
  |> Http.fromJson handleRequestDecoder


submitCmd: Model -> String -> Cmd Msg
submitCmd model api_url =
  Task.perform SubmitFail SubmitSuccess <| handleRequest model api_url


type Msg = SetUserId String | SetPassword String | SetTransferId String | SetApprove String | SubmitForm | SubmitFail Http.Error | SubmitSuccess (String, String, String) | SetInputState
update: Msg -> Model -> (Model, Cmd Msg) 
update msg model = 
  case msg of
    SetUserId userid -> ({model | userid = userid}, Cmd.none)
    SetPassword password -> ({model | password = password}, Cmd.none)
    SetTransferId transferid -> ({model | transferid = transferid}, Cmd.none)
    SetApprove approve -> ({model | approve = not model.approve}, Cmd.none)
    SubmitForm -> (model, submitCmd model handle_incoming_request_url) 
    SubmitFail error -> ({model | password = "", message = toString error}, Cmd.none)
    SubmitSuccess (return_status, return_balance, return_error) ->
      case return_error of 
        "" -> ({model | password = "", message = return_status ++ ", Current Balance: " ++ return_balance}, Cmd.none)
        _ -> ({model | password = "", message = return_error}, Cmd.none)
    SetInputState -> ({model | password = "", message = "Check Required Fields"}, Cmd.none)

-- VIEW
view: Model -> Html Msg
view model =
  div[]
    [ h2[][text "Gooble Gobble"]
    , navigation_bar
    , h3[][text "Handle Incoming Transfer Request"]
    , div[]
      [ label [ for "userid_field"] [ text "User Id " ]
      , input [ id "userid_field", type' "string", placeholder "Enter UserID", required True, onInput SetUserId ] []
      , validate_userid model
      , br [][]
      , label [ for "password_field"] [ text "Password " ]
      , input [ id "password_field", type' "password", placeholder "Enter Password", required True, Html.Attributes.value model.password, onInput SetPassword ] []
      , validate_password model
      , br [][]
      , label [ for "transferid_field"] [ text "Transfer Id " ]
      , input [ id "transferid_field", type' "string", placeholder "Enter TransferID", required True, onInput SetTransferId ] []
      , validate_transferid model
      , br [][]
      , label [ for "approve_field"] [ text "Approve? " ]
      , input [ id "approve_field", type' "checkbox", onClick (SetApprove "True") ] []
      , br [][]
      , button [onClick <| if valid_inputs model then SubmitForm else SetInputState][text "Handle Incoming Transfer"]
      ]
    , h3[][text model.message]
    ]


-- SUBSCRIPTIONS
subscriptions: Model -> Sub Msg
subscriptions model =
  Sub.none


-- VALIDATION

validate_password: Model -> Html Msg
validate_password model =
  let
    (password_state) =
      if model.password == "" then ("Password Required")
      else ("")
  in
    text password_state

validate_userid: Model -> Html Msg
validate_userid model =
  let
    (userid_state) =
      if model.userid == "" then ("UserID Required")
      else ("")
  in
    text userid_state

validate_transferid: Model -> Html Msg
validate_transferid model =
  let
    (transferid_state) =
      if model.transferid == "" then ("TransferID Required")
      else ("")
  in
    text transferid_state

valid_inputs: Model -> Bool
valid_inputs model =
  not (model.password == "" || model.userid == "" || model.transferid == "")

