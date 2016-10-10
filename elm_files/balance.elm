module Balance exposing (..)

import Html exposing (..)
import Html.App as App
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http exposing (..)
import Task exposing (Task)
import String 
import Json.Decode as Decode exposing (..)
import Json.Encode as Encode exposing (..)

import Navigation exposing (..)


main = App.program { init = init, view = view, update = update, subscriptions = subscriptions }


-- TYPES
type alias Model = { userid : String, password : String, message: String }
type Msg = SetUserId String | SetPassword String | SubmitForm | SubmitFail Http.Error | SubmitSuccess (String, String) | SetInputState


-- INIT
init: (Model, Cmd Msg)
init = (Model "" "" "", Cmd.none)


-- REST
balance_url: String
balance_url = "http://localhost:5000/balance"

userEncoder: Model -> Encode.Value
userEncoder model =
  Encode.object [("userid", Encode.string model.userid), ("password", Encode.string model.password)]

balanceDecoder: Decoder (String, String)
balanceDecoder = 
  Decode.object2 (,)
    ("Balance" := Decode.string)
    ("Error" := Decode.string)

checkBalance: Model -> String -> Task Http.Error (String, String)
checkBalance model api_url =
  {
    verb = "POST"
  , headers = [("Content-Type", "application/json")]
  , url = api_url
  , body = Http.string <| Encode.encode 0 <| userEncoder model
  }
  |> Http.send Http.defaultSettings
  |> Http.fromJson balanceDecoder

submitCmd: Model -> String -> Cmd Msg
submitCmd model api_url =
  Task.perform SubmitFail SubmitSuccess <| checkBalance model api_url


-- UPDATE
update: Msg -> Model -> (Model, Cmd Msg) 
update msg model = 
  case msg of
    SetUserId userid -> ({model | userid = userid}, Cmd.none)
    SetPassword password -> ({model | password = password}, Cmd.none)
    SubmitForm -> (model, submitCmd model balance_url) 
    SubmitFail error -> ({model | password = "", message = toString error}, Cmd.none)
    SubmitSuccess (return_balance, return_error) -> ({model | password = "", message = return_balance ++ return_error}, Cmd.none)
    SetInputState -> ({model | password = "", message = "Check Required Fields"}, Cmd.none)


-- VIEW
view: Model -> Html Msg
view model =
  div[]
    [ h2[][text "Gooble Gobble"]
    , navigation_bar
    , h3[][text "Check Balance"]
    , div[]
      [ label [ for "userid_field" ][ text "User Id " ]
      , input [ id "userid_field", type' "string", placeholder "Enter UserID", required True, onInput SetUserId ] []
      , validate_userid model
      , br [][]
      , label [ for "password_field" ][ text "Password " ]
      , input [ id "password_field", type' "password", placeholder "Enter Password", required True, Html.Attributes.value model.password,  onInput SetPassword ] []
      , validate_password model
      , br [][]
      , button [onClick <| if valid_inputs model then SubmitForm else SetInputState][text "Check Balance"]
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

valid_inputs: Model -> Bool
valid_inputs model =
  not (model.password == "" || model.userid == "")




