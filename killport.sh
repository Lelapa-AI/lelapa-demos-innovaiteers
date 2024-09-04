PORT=7000

PID=$(sudo lsof -t -i :$PORT)
if [ -z "$PID" ]; then
  echo "No process is using port $PORT."
  exit 0
fi
echo "Killing process with PID $PID using port $PORT."
sudo kill -9 $PID
if sudo lsof -i :$PORT > /dev/null; then
  echo "Port $PORT is still in use."
else
  echo "Port $PORT has been freed."
fi