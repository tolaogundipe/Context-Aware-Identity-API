import { useState } from "react";
import { login, getCurrentUser } from "../services/authService";
import { useNavigate } from "react-router-dom";


// login page component that handles user
//  authentication and then redirects to dashboard
function LoginPage() {

  // store user input and error state
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // navigation hook for redirecting after login
  const navigate = useNavigate();


  // sends login request, stores tokens, fetches user data,
  // and redirects to dashboard
  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // authenticate user and get jwt tokens
      const data = await login(username, password);

      // store tokens in local storage
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);

      // fetch current user using access token
      const user = await getCurrentUser(data.access);

      // store user role for later use
      localStorage.setItem("role", user.role.name);

      // redirect to dashboard
      navigate("/dashboard");
    } catch (err) {
      // show error if login fails
      setError("Invalid credentials");
    }
  };

  // render login ui, it includes branding,
  // input fields, and login form
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">

      {/* APP TITLE / BRANDING */}
      <h1 className="text-3xl font-bold text-gray-800 mb-2">
        Context-Aware Identity API
      </h1>
      <p className="text-gray-500 mb-8 text-sm">
        Secure identity resolution with role-based access
      </p>

      {/* LOGIN FORM */}
      <form
        onSubmit={handleLogin}
        className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 w-96"
      >
        <h2 className="text-xl font-semibold mb-6 text-center text-gray-700">
          Sign in to your account
        </h2>

        {/* ERROR MESSAGE */}
        {error && (
          <p className="text-red-500 mb-4 text-sm text-center">{error}</p>
        )}

        {/* USERNAME INPUT */}
        <input
          type="text"
          placeholder="Username"
          className="w-full border border-gray-300 p-2.5 mb-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        {/* PASSWORD INPUT */}
        <input
          type="password"
          placeholder="Password"
          className="w-full border border-gray-300 p-2.5 mb-6 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {/* LOGIN BUTTON */}
        <button className="w-full bg-gray-900 text-white p-2.5 rounded-lg hover:bg-gray-800 transition">
          Login
        </button>
      </form>
    </div>
  );
}

export default LoginPage;