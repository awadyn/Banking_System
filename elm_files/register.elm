module Register exposing (..)

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


-- APP
main = App.program { init = init, view = view, update = update, subscriptions = subscriptions }


-- TYPES
type alias Model = { password : String, confirm_password : String, message: String }
type Msg = SetPassword String | SetConfirmPassword String | SubmitForm | SubmitFail Http.Error | SubmitSuccess (String, String) | SetInputState


-- INIT
init: (Model, Cmd Msg)
init = (Model "" "" "", Cmd.none)


-- REST
register_url: String
register_url = "http://localhost:5000/register"

userEncoder: Model -> Encode.Value
userEncoder model =
  Encode.object [("password", Encode.string model.password), ("confirm_password", Encode.string model.confirm_password)]

userDecoder: Decoder (String, String)
userDecoder = 
  Decode.object2 (,)
    ("New User" := Decode.string)
    ("Error" := Decode.string)

registerUser: Model -> String -> Task Http.Error (String, String)
registerUser model api_url =
  {
    verb = "POST"
  , headers = [("Content-Type", "application/json")]
  , url = api_url
  , body = Http.string <| Encode.encode 0 <| userEncoder model
  }
  |> Http.send Http.defaultSettings
  |> Http.fromJson userDecoder

submitCmd: Model -> String -> Cmd Msg
submitCmd model api_url =
  Task.perform SubmitFail SubmitSuccess <| registerUser model api_url


-- UPDATE
update: Msg -> Model -> (Model, Cmd Msg) 
update msg model = 
  case msg of
    SetPassword password -> ({model | password = password}, Cmd.none)
    SetConfirmPassword confirm_password -> ({model | confirm_password = confirm_password}, Cmd.none)
    SubmitForm -> (model, submitCmd model register_url) 
    SubmitFail error -> ({model | password = "", confirm_password = "", message = toString error}, Cmd.none)
    SubmitSuccess (return_user, return_error) -> ({model | password= "", confirm_password = "", message = return_user ++ return_error}, Cmd.none)
    SetInputState -> ({model | password = "", confirm_password = "", message = "Check Required Fields"}, Cmd.none)


-- VIEW
view: Model -> Html Msg
view model =
  div[]
    [ h2[][text "Gooble Gobble"]
    , navigation_bar
    , h3[][text "Register"]
    , div[]
      [ label [ for "password_field" ][ text "Password " ]
      , input [ id "password_field", type' "password", placeholder "Enter Password", required True,  Html.Attributes.value model.password, onInput SetPassword ] []
      , validate_password model
      , br [][]
      , label [ for "confirm_field" ][ text "Confirm Password " ]
      , input [ id "confirm_field", type' "password", placeholder "Confirm Password", required True, Html.Attributes.value model.confirm_password, onInput SetConfirmPassword ] []
      , validate_confirm model
      , br [][]
      , button [onClick <| if valid_inputs model then SubmitForm else SetInputState][text "Register"]
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

validate_confirm: Model -> Html Msg
validate_confirm model =
  let
    (confirm_state) =
      if model.password == model.confirm_password then ("")
      else ("Passwords Don't Match")
  in
    text confirm_state

valid_inputs: Model -> Bool
valid_inputs model =
  not (model.password == "" || model.password /= model.confirm_password)
  


