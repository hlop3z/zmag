import { useState, useEffect } from "preact/hooks";

const fakeQuery = {
  query: { page: 1, limit: 10, sort_by: ["-id", "name"] },
  filters: [{ id: { eq: 1 }, name: { in: ["john", "jane"] } }],
};

export function App() {
  const [user, setUser] = useState<Record<string, unknown> | null>(null);
  const [data, setData] = useState<unknown>(null);

  useEffect(() => {
    API.get("/auth/me")
      .then(setUser)
      .catch(async () => {
        await API.post("/auth/logout").catch(() => {});
      });
  }, []);

  async function logout() {
    await API.post("/auth/logout");
    window.location.href = "/";
  }

  async function testPublic() {
    const result = await API.get("/public/auth/model", fakeQuery);
    setData(result);
  }

  async function testSecret() {
    const result = await API.get("/v1/auth/model", fakeQuery);
    setData(result);
  }

  if (!user) return null;

  return (
    <main>
      <h1>Application View</h1>
      <p class="user">
        Logged in as <strong>{String(user.username)}</strong>
      </p>
      <button onClick={logout}>Logout</button>
      <button onClick={testSecret}>Test App</button>
      <button onClick={testPublic}>Test Pub</button>
      {data && (
        <pre style={{ textAlign: "left" }}>{JSON.stringify(data, null, 2)}</pre>
      )}
    </main>
  );
}
