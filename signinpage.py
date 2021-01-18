
def index():
    query_params = {
        client_id: '33d36c75c90f4c6897e6c9f62d71d3cb',
        response_type: "code",
        redirect_uri: "http://127.0.0.1:5000/signin",
        scope: "user-library-read user-library-modify playlist-modify-public user-top-read playlist-modify-public user-modify-playback-state user-follow-modify user-read-currently-playing user-read-playback-state user-follow-rad app-remote-control streaming user-read-birthdate user-read-email user-read-private",
        show_dialog: true
    }

    url = "https://accounts.spotify.com/authorize"
    redirect_to "#{url}?#{query_params.to_query}"



def create():
    if params[:error]:
        puts 'LOGIN ERROR', params
        redirect_to "http://127.0.0.1:5000/signin"
    else:
        body = {
        grant_type: "authorization_code",
        code: params[:code],
        redirect_uri: 'http://127.0.0.1:5000/signin'
        client_id='33d36c75c90f4c6897e6c9f62d71d3cb'
        client_secret='340a5398a57e4eacb0a530e921c8dca3'
        }
        auth_response = RestClient.post('https://accounts.spotify.com/api/token', body)
        auth_params = JSON.parse(auth_response.body)
        header = {
            Authorization: "Bearer #{auth_params["access_token"]}"
        }
        user_response = RestClient.get("https://api.spotify.com/v1/me", header)
        user_params = JSON.parse(user_response.body)
    @user = User.find_or_create_by(username: user_params["id"],
        spotify_url: user_params["external_urls"]["spotify"],
        href: user_params["href"],
        uri: user_params['uri'])
    @user.update(access_token: auth_params['access_token'], refresh_token: auth_params['refresh_token'])
    User.update_all(logged_in: false)
    @user.update(logged_in: true)
    ENV["CURRENT_USER_ID"] = @user.id.to_s
    ENV["SPOTIFY_USER_ID"] = @user.username
    redirect_to "http://127.0.0.1:5000/welcome"
