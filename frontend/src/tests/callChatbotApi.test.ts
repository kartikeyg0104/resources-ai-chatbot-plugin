import fetchMock from "jest-fetch-mock";
import { callChatbotApi } from "../utils/callChatbotApi";
import { API_BASE_URL } from "../config";
import { openChatbotStream } from "../utils/callChatbotApi";

class MockWebSocket {
  static OPEN = 1;
  static CLOSED = 3;
  readyState = 0;
  url: string;
  onopen: (() => void) | null = null;
  onmessage: ((ev: MessageEvent) => void) | null = null;
  onerror: ((ev: Event) => void) | null = null;
  onclose: ((ev: CloseEvent) => void) | null = null;
  sent: string[] = [];
  private listeners: Record<string, Function[]> = {};
  constructor(url: string) {
    this.url = url;
    ;(global as any).__lastWS = this;
    setTimeout(() => {
      this.readyState = MockWebSocket.OPEN;
      this.onopen && this.onopen();
      this.dispatchEvent("open", {});
    }, 0);
  }
  addEventListener(type: string, handler: any) {
    if (!this.listeners[type]) this.listeners[type] = [];
    this.listeners[type].push(handler);
  }
  removeEventListener(type: string, handler: any) {
    if (!this.listeners[type]) return;
    this.listeners[type] = this.listeners[type].filter((h) => h !== handler);
  }
  dispatchEvent(type: string, event: any) {
    (this.listeners[type] || []).forEach((h) => h(event));
  }
  send(data: string) {
    this.sent.push(data);
  }
  close() {
    this.readyState = MockWebSocket.CLOSED;
    this.onclose && this.onclose({} as CloseEvent);
    this.dispatchEvent("close", {});
  }
}

// @ts-ignore
global.WebSocket = MockWebSocket;

test("openChatbotStream streams tokens and end", (done) => {
  const tokens: string[] = [];
  const { send } = openChatbotStream(
    "session-123",
    (msg) => {
      if (msg.type === "token") tokens.push(msg.token);
      if (msg.type === "end") {
        expect(tokens.join("")).toBe("hello world");
        done();
      }
    },
  );

  // The send should not throw even if not yet open
  send("hi");

  const getWS = () => (global as any).__lastWS as MockWebSocket;
  const dispatch = (payload: any) => {
    const ws = getWS();
    ws.onmessage && ws.onmessage({ data: JSON.stringify(payload) } as MessageEvent);
  };

  setTimeout(() => {
    dispatch({ token: "hello " });
    dispatch({ token: "world" });
    dispatch({ end: true });
  }, 1);
});

describe("callChatbotApi", () => {
  beforeEach(() => {
    fetchMock.resetMocks();
  });

  it("returns parsed JSON when response is ok", async () => {
    const mockData = { reply: "Hello" };
    fetchMock.mockResponseOnce(JSON.stringify(mockData));

    const result = await callChatbotApi(
      "some-endpoint",
      {},
      { fallback: true },
      5000,
    );

    expect(result).toEqual(mockData);

    expect(fetchMock).toHaveBeenCalledWith(
      `${API_BASE_URL}/api/chatbot/some-endpoint`,
      expect.objectContaining({
        signal: expect.any(Object),
      }),
    );
  });

  it("returns fallback value when response is not ok", async () => {
    fetchMock.mockResponseOnce("Internal error", { status: 500 });

    const fallback = { error: "fallback" };
    const result = await callChatbotApi("bad-endpoint", {}, fallback, 5000);

    expect(result).toBe(fallback);
  });

  it("returns fallback value when fetch throws", async () => {
    fetchMock.mockRejectOnce(new Error("Network error"));

    const fallback = { error: "network" };
    const result = await callChatbotApi("error-endpoint", {}, fallback, 5000);

    expect(result).toBe(fallback);
  });

  it("returns fallback value when request times out (AbortError)", async () => {
    const abortError = { name: "AbortError" };

    fetchMock.mockRejectedValueOnce(abortError);

    const fallback = { error: "timeout" };
    const result = await callChatbotApi("timeout-endpoint", {}, fallback, 10);

    expect(result).toBe(fallback);
  });
});
