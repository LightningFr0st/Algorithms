using SFML.Graphics;
using SFML.System;
using SFML.Window;
using System;
using System.Collections.Generic;

namespace Lab3
{
    internal class Program
    {
        static void OnClose(object sender, EventArgs e)
        {
            RenderWindow window = (RenderWindow)sender;
            window.Close();
        }
        static double GetGaussY(double x, double mean, double deviation)
        {
            return 1 / (deviation * Math.Sqrt(2 * Math.PI)) * Math.Exp(-0.5 * Math.Pow((x - mean) / deviation, 2));
        }
        static double GetMean(List<double> values)
        {
            double mean = 0;
            foreach (var value in values)
                mean += value;
            return mean / values.Count;
        }
        static double GetVariance(List<double> values)
        {
            double variance = 0, mean = GetMean(values);
            foreach (var value in values)
                variance += Math.Pow(value - mean, 2);
            return variance / values.Count;
        }
        static double NextGauss(double mean, double deviation)
        {
            Random rand = new Random();
            double u1 = 1.0 - rand.NextDouble();
            double u2 = 1.0 - rand.NextDouble();
            double normalRandom = Math.Sqrt(-2.0 * Math.Log(u1)) * Math.Sin(2.0 * Math.PI * u2);
            return mean + deviation * normalRandom;
        }
        static void FillList(int count, ref List<double> value, double mean, double deviation)
        {
            for (int i = 0; i < count; i++)
                value.Add(NextGauss(mean, deviation));
        }
        static List<double> MergeLists(List<double> vector1, List<double> vector2)
        {
            var newList = new List<double>();
            newList.AddRange(vector1);
            newList.AddRange(vector2);
            return newList;
        }
        static List<double> GetInterval(List<double> values)
        {
            var interval = new List<double>();
            interval.Add(values.Min());
            interval.Add(values.Max());
            return interval;
        }
        static int FindSeparatorIndex(List<double> y1Values, List<double> y2Values, List<double> xValues)
        {
            bool firstIsBigger = y1Values[0] > y2Values[0];
            int separatorI = 0;

            for (int i = 0; i < xValues.Count; i++)
            {
                if ((firstIsBigger && y2Values[i] >= y1Values[i]) || (!firstIsBigger && y1Values[i] > y2Values[i]))
                {
                    separatorI = i;
                    break;
                }
            }
            return separatorI;
        }
        static List<double> GetDoublesFromRange(double start, double end, double step)
        {
            List<double> values = new List<double>();
            while (start <= end)
            {
                values.Add(start);
                start += step;
            }
            return values;
        }
        static double NextY(double x, double mean, double deviation, double probability)
        {
            return GetGaussY(x, mean, deviation) * probability;
        }
        static List<double> GetYList(List<double> x, double mean, double deviation, double probability)
        {
            List<double> y = new List<double>();
            foreach (double value in x)
                y.Add(NextY(value, mean, deviation, probability));
            return y;
        }
        public static List<double> GetAreas(List<double> y1Values, List<double> y2Values, double step, List<double> xValues)
        {
            double falseAlarm = 0;
            double detectionMistake = 0;

            int separator = FindSeparatorIndex(y1Values, y2Values, xValues);

            for (int i = 0; i < separator; i++)
            {
                falseAlarm += step * y2Values[i];
            }

            for (int i = separator; i < xValues.Count; i++)
            {
                detectionMistake += step * y1Values[i];
            }

            List<double> areas = new() { detectionMistake, falseAlarm };
            return areas;
        }

        static void Main()
        {
            double mean1, mean2, deviation1, deviation2, probability1, probability2;

            Console.WriteLine("Размер выборки:");
            int size = int.Parse(Console.ReadLine());

            Console.WriteLine("Mx1");
            mean1 = double.Parse(Console.ReadLine());

            Console.WriteLine("Mx2");
            mean2 = double.Parse(Console.ReadLine());

            Console.WriteLine("Dx1");
            deviation1 = double.Parse(Console.ReadLine());

            Console.WriteLine("Dx2");
            deviation2 = double.Parse(Console.ReadLine());

            Console.WriteLine("P1");
            probability1 = double.Parse(Console.ReadLine());
            probability2 = 1 - probability1;
            Console.WriteLine($"P2 {probability2}");

            double step = 0.001;

            List<double> vector1 = new List<double>();
            FillList(size, ref vector1, mean1, deviation1);
            List<double> vector2 = new List<double>();
            FillList(size, ref vector2, mean2, deviation2);

            var interval = GetInterval(MergeLists(vector1, vector2));
            var x = GetDoublesFromRange(interval[0], interval[1], step);

            var y1 = GetYList(x, GetMean(vector1), Math.Sqrt(GetVariance(vector1)), probability1);
            var y2 = GetYList(x, GetMean(vector2), Math.Sqrt(GetVariance(vector2)), probability2);

            List<double> areas = GetAreas(y1, y2, step, x);
            Console.WriteLine($"Ложная тревога {areas[0]}");
            Console.WriteLine($"Ошибка обнаружения {areas[1]}");
            Console.WriteLine($"Суммарная ошибка классификации {areas[0] + areas[1]}");
            CircleShape point = new CircleShape(1);

            RenderWindow window = new(new VideoMode(1920, 1080), "Output");
            window.SetFramerateLimit(60);
            window.Closed += new EventHandler(OnClose);

            while (window.IsOpen)
            {

                window.DispatchEvents();
                window.Clear(Color.Black);
                for (int i = 0; i < x.Count; i++)
                {
                    point.FillColor = Color.White;
                    point.Position = new Vector2f((float)(600 - 100 * x[i]), (float)((1 - y1[i]) * 500));
                    window.Draw(point);
                    point.FillColor = Color.Green;
                    point.Position = new Vector2f((float)(600 - 100 * x[i]), (float)((1 - y2[i]) * 500));
                    window.Draw(point);
                }
                window.Display();
            }
        }
    }
}
/*
100
-1
1
1
1,5
0,4
*/