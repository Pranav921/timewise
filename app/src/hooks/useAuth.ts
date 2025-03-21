import { useEffect, useRef, useState } from "react";
import { onAuthStateChanged, User } from "firebase/auth";
import { auth } from "../firebase";
import { dataClient } from "../dataClient";
// import { router } from "../router";

export const useAuth = () => {
  // const [user, setUser] = useState<User | null>(null);
  // const [loading, setLoading] = useState(true);
  // https://github.com/TanStack/router/discussions/1668#discussioncomment-10634735
  // we can use this to "await" for the auth state to be fulfilled (finished loading) so that the user don't see
  // a flash of the login page when they are already logged in
  // also, can't we just use a global variable here instead of a ref
  const authPromiseRef = useRef<PromiseWithResolvers<User | null>>(undefined);
  if (!authPromiseRef.current) {
    authPromiseRef.current = Promise.withResolvers<User | null>();
  }

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      // these 3 lines are sort of useless? probably will remove them later and just only expose the authPromise
      // setUser(currentUser);
      // setLoading(false);
      // router.invalidate();

      authPromiseRef.current!.resolve(currentUser);
      dataClient.setLoggedInStatus(!!currentUser);
    });
    return () => unsubscribe();
  }, []);

  // this function is needed so that the authPromise is updated with the newly logged in user.
  // Because the old promise will be already resolved and have a stale value, a new promise with the updated value is needed
  const updateAuthPromiseAfterLogin = (user: User) => {
    authPromiseRef.current = Promise.withResolvers<User | null>();
    authPromiseRef.current.resolve(user);
    dataClient.setLoggedInStatus(true);
  };

  return {
    // user,
    // loading,
    authPromise: authPromiseRef,
    updateAuthPromiseAfterLogin,
  };
};
