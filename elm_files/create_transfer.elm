module Create_Transfer exposing (..)

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
type alias Model = { sourceid : String, password : String, destid : String, amount : Int, transfer_message : String, message: String }


-- INIT
init: (Model, Cmd Msg)
init = (Model "" "" "" -1 "" "", Cmd.none)


-- UPDATE
create_transfer_url: String
create_transfer_url = "http://localhost:5000/create_transfer"


transferRequestEncoder: Model -> Encode.Value
transferRequestEncoder model =
  Encode.object [("sourceid", Encode.string model.sourceid), ("password", Encode.string model.password), ("destid", Encode.string model.destid), ("amount", Encode.int model.amount), ("transfer_message", Encode.string model.transfer_message)]


transfersDecoder: Decoder (String, String)
transfersDecoder =
  Decode.object2 (,)
    ("New Transfer" := Decode.string)
    ("Error" := Decode.string)


createTransfer: Model -> String -> Task Http.Error (String, String)
createTransfer model api_url =
  {
    verb = "POST"
  , headers = [("Content-Type", "application/json")]
  , url = api_url
  , body = Http.string <| Encode.encode 0 <| transferRequestEncoder model
  }
  |> Http.send Http.defaultSettings
  |> Http.fromJson transfersDecoder


submitCmd: Model -> String -> Cmd Msg
submitCmd model api_url =
  Task.perform SubmitFail SubmitSuccess <| createTransfer model api_url


type Msg = SetSourceId String | SetPassword String | SetDestId String | SetAmount String | SetTransferMessage String | SubmitForm | SubmitFail Http.Error | SubmitSuccess (String, String) | SetInputState

represent_amount: Int -> String
represent_amount amount =
  case amount of
    -1 -> ""
    _ -> toString amount

update: Msg -> Model -> (Model, Cmd Msg) 
update msg model = 
  case msg of
    SetSourceId sourceid -> ({model | sourceid = sourceid}, Cmd.none)
    SetPassword password -> ({model | password = password}, Cmd.none)
    SetDestId destid -> ({model | destid = destid}, Cmd.none)
    SetAmount amount -> 
      case toInt amount of
        Ok val -> ({model | amount = val}, Cmd.none)
        Err err -> (model, Cmd.none)
    SetTransferMessage transfer_message -> ({model | transfer_message = transfer_message}, Cmd.none)
    SubmitForm -> (model, submitCmd model create_transfer_url) 
    SubmitFail error -> ({model | password = "", amount = -1, message = toString error}, Cmd.none)
    SubmitSuccess (return_transfer, return_error) -> ({model | password = "", amount = -1, message = return_transfer ++ return_error}, Cmd.none)
    SetInputState -> ({model | password = "", message = "Check Required Fields"}, Cmd.none)

-- VIEW
view: Model -> Html Msg
view model =
  div[]
    [ h2[][text "Gooble Gobble"]
    , navigation_bar
    , h3[][text "Create Transfer"]
    , div [ id "create_transfer_form" ]
      [ label [ for "sourceid_field"] [ text "User ID " ]
      , input [ id "sourceid_field", type' "string", placeholder "Enter SourceID", required True, onInput SetSourceId ] []
      , validate_sourceid model
      , br [][]
      , label [ for "password_field"] [ text "Password " ]
      , input [ id "password_field", type' "password", placeholder "Enter Password", required True,  Html.Attributes.value model.password, onInput SetPassword ] []
      , validate_password model
      , br [][]
      , label [ for "destid_field"] [ text "Destination ID " ]
      , input [ id "destid_field", type' "string", placeholder "Enter DestID", required True, onInput SetDestId ] []
      , validate_destid model
      , br [][]
      , label [ for "amount_field"] [ text "Amount " ]
      , input [ id "amount_field", type' "string", placeholder "Enter Amount", required True, Html.Attributes.value (represent_amount model.amount), onInput SetAmount ] []
      , validate_amount model
      , br [][]
      , label [ for "message_field"] [ text "Transfer Message " ]
      , textarea [ id "message_field", placeholder "Transfer Message", maxlength 30, onInput SetTransferMessage ] []
      , br [][]
      , button [onClick <| if valid_inputs model then SubmitForm else SetInputState][text "Create Transfer"]
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

validate_sourceid: Model -> Html Msg
validate_sourceid model =
  let
    (sourceid_state) =
      if model.sourceid == "" then ("SourceID Required")
      else ("")
  in
    text sourceid_state

validate_destid: Model -> Html Msg
validate_destid model =
  let
    (destid_state) =
      if model.destid == "" then ("DestinationID Required")
      else ("")
  in
    text destid_state

validate_amount: Model -> Html Msg
validate_amount model =
  let
    (amount_state) =
      if model.amount == -1 then ("Amount Required")
      else ("")
  in
    text amount_state

valid_inputs: Model -> Bool
valid_inputs model =
  not (model.password == "" || model.sourceid == "" || model.destid == "" || model.amount == -1)


