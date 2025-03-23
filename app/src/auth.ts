import { auth } from "./firebase";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
} from "firebase/auth";

export const register = async (email: string, password: string) => {
  try {
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      email,
      password
    );
    console.log("User signed up:", userCredential.user);
    await loginToBackend();
  } catch (error: any) {
    console.error("Error signing up:", error.message);
  }
};

export const logIn = async (email: string, password: string) => {
  try {
    const userCredential = await signInWithEmailAndPassword(
      auth,
      email,
      password
    );
    console.log("User signed in:", userCredential.user);
    await loginToBackend();
  } catch (error: any) {
    console.error("Error signing in:", error.message);
  }
};

export const logOut = async () => {
  try {
    await signOut(auth);
    console.log("User signed out");
  } catch (error: any) {
    console.error("Error signing out:", error.message);
  }
};

export const getFirebaseToken = async (): Promise<string | null> => {
  const user = auth.currentUser;
  return user ? await user.getIdToken() : null;
};

export const loginToBackend = async () => {
  const token = await getFirebaseToken();
  if (!token) {
    console.error("No Firebase token found");
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/api/auth/login", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    console.log("Backend login success:", data);
  } catch (error) {
    console.error("Error logging into backend:", error);
  }
};
