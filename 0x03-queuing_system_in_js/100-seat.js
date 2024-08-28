import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

// Create Redis client and promisify
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Initialize Kue queue
const queue = kue.createQueue();

const app = express();
const port = 1245;
const reservationEnabled = true;

// Function to reserve seats
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Function to get current available seats
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10);
}

// Initialize available seats to 50
reserveSeat(50);

// Create and queue a reservation job
function createReservationJob() {
  return new Promise((resolve, reject) => {
    // eslint-disable-next-line consistent-return
    const job = queue.create('reserve_seat').save((err) => {
      if (err) return reject(err);
      resolve(job.id);
    });
  });
}

// Process the queue
async function processQueue() {
  queue.process('reserve_seat', async (job, done) => {
    try {
      const availableSeats = await getCurrentAvailableSeats();
      if (availableSeats <= 0) {
        done(new Error('Not enough seats available'));
        return;
      }

      await reserveSeat(availableSeats - 1);
      done();
    } catch (error) {
      done(error);
    }
  });
}

// Express server routes
app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats.toString() });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  try {
    const jobId = await createReservationJob();
    res.json({ status: 'Reservation in process' });

    // Handle job completion
    kue.Job.get(jobId, (err, job) => {
      if (err) console.log(`Error fetching job: ${err.message}`);
      job.on('complete', () => console.log(`Seat reservation job ${jobId} completed`));
      job.on('failed', (errorMessage) => console.log(`Seat reservation job ${jobId} failed: ${errorMessage}`));
    });
  } catch (error) {
    res.json({ status: 'Reservation failed' });
  }
});

app.get('/process', async (req, res) => {
  await processQueue();
  res.json({ status: 'Queue processing' });
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
