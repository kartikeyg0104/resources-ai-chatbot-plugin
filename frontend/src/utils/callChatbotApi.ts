import { API_BASE_URL, WS_BASE_URL } from "../config";

/**
 * Generic utility to call chatbot API endpoints.
 *
 * @param endpoint - The path after `/api/chatbot/`
 * @param options - Fetch options like method, headers, body
 * @param fallbackErrorValue - Value to return in case of failure
 * @param timeoutMs - Value of the timeout after which the request is aborted
 * @returns A Promise resolving to the parsed JSON or fallback value
 */
export const callChatbotApi = async <T>(
  endpoint: string,
  options: RequestInit,
  fallbackErrorValue: T,
  timeoutMs: number,
): Promise<T> => {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${API_BASE_URL}/api/chatbot/${endpoint}`, {
      ...options,
      signal: controller.signal,
    });

    if (!response.ok) {
      console.error(`API error: ${response.status} ${response.statusText}`);
      return fallbackErrorValue;
    }

    return await response.json();
  } catch (error: unknown) {
    if (error instanceof DOMException && error.name == "AbortError") {
      console.error(
        `API request to ${endpoint} timed out aftr ${timeoutMs}ms.`,
      );
    } else {
      console.error(`API error calling ${endpoint}:`, error);
    }
    return fallbackErrorValue;
  } finally {
    clearTimeout(id);
  }
};

export type StreamMessage =
  | { type: "token"; token: string }
  | { type: "end" }
  | { type: "error"; error: string };

/**
 * Connects to the WebSocket streaming endpoint and yields tokens as they arrive.
 * The consumer is responsible for closing the socket via the returned close function.
 */
export const openChatbotStream = (
  sessionId: string,
  onMessage: (msg: StreamMessage) => void,
  onOpen?: () => void,
  onClose?: (ev: CloseEvent) => void,
  onError?: (ev: Event) => void,
): { send: (message: string) => void; close: () => void; socket: WebSocket } => {
  const url = `${WS_BASE_URL.replace(/\/$/, "")}/api/chatbot/sessions/${sessionId}/stream`;
  const socket = new WebSocket(url);

  socket.onopen = () => {
    onOpen && onOpen();
  };

  socket.onmessage = (event: MessageEvent) => {
    try {
      const data = JSON.parse(String(event.data));
      if (data.token !== undefined) {
        onMessage({ type: "token", token: data.token });
      } else if (data.end) {
        onMessage({ type: "end" });
      } else if (data.error) {
        onMessage({ type: "error", error: String(data.error) });
      }
    } catch (e) {
      onMessage({ type: "error", error: "Invalid message format" });
    }
  };

  socket.onerror = (ev: Event) => {
    onError && onError(ev);
  };

  socket.onclose = (ev: CloseEvent) => {
    onClose && onClose(ev);
  };

  const send = (message: string) => {
    if (socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ message }));
    } else {
      const handleOpen = () => {
        socket.send(JSON.stringify({ message }));
        socket.removeEventListener("open", handleOpen as any);
      };
      socket.addEventListener("open", handleOpen as any);
    }
  };

  const close = () => socket.close();

  return { send, close, socket };
};
