using System;
using System.IO;
using System.Text;

using System.Diagnostics;
using System.Timers;

namespace ProcessMonitor
{

    class Program
    {
        static void Main(string[] args)
        {
            // Display the number of command line arguments.
            Console.WriteLine(args.Length);

            // Test if input arguments were supplied.
            if (args.Length == 0)
            {
                Console.WriteLine("Please enter a process name.");
                //throw new ArgumentNullException("Cannot be null or empty",args);
            }
            else
            {
                // The process name to monitor
                string processName = args[0];
                string logFilePath = args[3];
                StringBuilder sb = new StringBuilder();
                
                // The threshold (in seconds) after which the process will be killed
                int thresholdSeconds = 0;

                // The watchdog time interval used to check if the process is still running
                int timeFrequency = 0;

                // Try to convert the input arguments to numbers. This will throw
                // an exception if the argument is not a number.
                int num1;
                bool runTimeThreshold = int.TryParse(args[1], out num1);
                if (!runTimeThreshold)
                {
                    Console.WriteLine("Please enter a process run time threshold.");
                    Console.WriteLine("Usage: Factorial <num>");
                    //return 1;
                    //throw new ArgumentException("Cannot be null or empty", args[1]);
                }
                else
                {
                    thresholdSeconds = int.Parse(args[1]);
                }

                int num2;
                bool TimeFrequency = int.TryParse(args[2], out num2);
                if (!TimeFrequency)
                {
                    Console.WriteLine("Please enter a test time frequency.");
                    Console.WriteLine("Usage: Factorial <num>");
                    //throw new ArgumentException("Cannot be null or empty", args[2]);
                }
                else
                {
                    timeFrequency = int.Parse(args[2]);
                }


                // Create a timer with a second interval
                var timer = new Timer(timeFrequency);
                // Hook up the Elapsed event for the timer 
                timer.Elapsed += OnTimedEvent;
                // Start the timer 
                timer.Start();


                while (true)
                {
                    // Get all running processes with the specified name
                    Process[] processes = Process.GetProcessesByName(processName);

                    // Loop through each process
                    foreach (Process process in processes)
                    {
                        // Calculate the time elapsed since the process started
                        TimeSpan elapsed = DateTime.Now - process.StartTime;

                        // If the elapsed time is greater than the threshold, kill the process
                        if (elapsed.TotalSeconds > thresholdSeconds)
                        {
                            Console.WriteLine("Killing process: {0} (PID: {1})", process.ProcessName, process.Id);
                            process.Kill();

                            sb.Append("Killing process: {0} (PID: {1})");
                            sb.AppendFormat("{0,12:X4} {1,12}", process.ProcessName, Convert.ToChar(process.Id));
                            sb.AppendLine();                            
                        }
                    }

                    // Wait for 1 second before checking the processes again
                    System.Threading.Thread.Sleep(1000);
                }

                Console.WriteLine(sb.ToString());      
                File.AppendAllText(logFilePath, sb.ToString());
                //sb.Clear();

                // Keep the program running until the user presses a key
                Console.ReadKey();

            }
            

        }

        private static void OnTimedEvent(object source, ElapsedEventArgs e)
        {
            // This code will run every 1 second
            Console.WriteLine("Main() function is running periodically.");
        }
                
    }
}