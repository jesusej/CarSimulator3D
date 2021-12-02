using System;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

public class SocketComponent : MonoBehaviour
{
    static Socket listener;
    private CancellationTokenSource tokenSource;
    public ManualResetEvent manualResetEvent;
    public Transform target;
    readonly int PORT = 3000;
    readonly int TIMEOUT = 1;
    Vector3 tempPosition = new Vector3();

    async void Start()
    {
        tokenSource = new CancellationTokenSource();
        manualResetEvent = new ManualResetEvent(false);
        await Task.Run(() => ListenEvents(tokenSource.Token));
    }

    void Update()
    {
        target.position = tempPosition;
    }

    private void ListenEvents(CancellationToken token)
    {
        IPHostEntry ipHostEntry = Dns.GetHostEntry(Dns.GetHostName());
        IPAddress ipAddress = ipHostEntry.AddressList.FirstOrDefault(ip => ip.AddressFamily == AddressFamily.InterNetwork);
        IPEndPoint ipEndPoint = new IPEndPoint(ipAddress, PORT);
        listener = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

        try
        {
            listener.Bind(ipEndPoint);
            listener.Listen(10);

            while (!token.IsCancellationRequested)
            {
                manualResetEvent.Reset();

                Debug.Log("Waiting connection to host " + ipAddress.MapToIPv4().ToString() + " : " + PORT);
                listener.BeginAccept(new AsyncCallback(Callback), listener);

                while (!token.IsCancellationRequested)
                {
                    if (manualResetEvent.WaitOne(TIMEOUT))
                    {
                        break;
                    }
                }

            }
        }
        catch (Exception e)
        {
            Debug.Log(e.ToString());
        }
    }

    void Callback(IAsyncResult result)
    {
        Socket listener = (Socket)result.AsyncState;
        Socket handler = listener.EndAccept(result);

        manualResetEvent.Set();

        StateObject state = new StateObject();
        state.socket = handler;
        handler.BeginReceive(state.buffer, 0, StateObject.BUFFERSIZE, 0, new AsyncCallback(ReadCallback), state);
    }

    void ReadCallback(IAsyncResult result)
    {
        StateObject state = (StateObject)result.AsyncState;
        Socket handler = state.socket;

        int read = handler.EndReceive(result);

        if (read > 0)
        {
            state.positionString.Append(Encoding.ASCII.GetString(state.buffer, 0, read));
            handler.BeginReceive(state.buffer, 0, StateObject.BUFFERSIZE, 0, new AsyncCallback(ReadCallback), state);
        }
        else
        {
            if (state.positionString.Length > 1)
            {
                string content = state.positionString.ToString();
                Debug.Log($"Read {content.Length} bytes.\nInfo : {content}");
                SetPosition(content);
            }
            handler.Close();
        }
    }

    void SetPosition(string positionString)
    {
        string[] components = positionString.Split(',');
        Vector3 position = new Vector3(
            float.Parse(components[0]),
            float.Parse(components[1]),
            float.Parse(components[2])
        );
        tempPosition = position;
    }

    void OnDestroy()
    {
        tokenSource.Cancel();
    }

    public class StateObject
    {
        public Socket socket = null;
        public const int BUFFERSIZE = 1024;
        public byte[] buffer = new byte[BUFFERSIZE];
        public StringBuilder positionString = new StringBuilder();
    }
}
