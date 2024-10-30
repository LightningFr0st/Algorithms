using Microsoft.VisualBasic.ApplicationServices;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace lab5_MODI
{
    internal class Calculations
    {
        public int objects;

        int[] templ = { 4, 4, 16 };

        public int[] func = { 0, 0, 0, 0 };

        public (int, int)[] obj;

        public int it = 0;

        public Calculations(int p_obj = 4)
        {
            Random rnd = new Random();
            objects = p_obj;
            obj = new (int, int)[objects + 1];
            for (int i = 1; i <= objects / 2; i++)
            {
                obj[i] = (rnd.Next(-10, 10), rnd.Next(-10, 10));
                obj[i + objects / 2] = (rnd.Next(-10, 10), rnd.Next(-10, 10));
            }
            while (it != objects - 1)
            {
                calc(obj[it].Item1, obj[it].Item2);
                it++;
            }
        }

        public void calc(int x1, int x2)
        {
            int[] templ = { 1, 4, 4, 16 };
            templ[1] *= x1;
            templ[2] *= x2;
            templ[3] *= x1 * x2;

            int res = func[0] + func[1] * obj[it + 1].Item1 + func[2] * obj[it + 1].Item2 + func[3] * obj[it + 1].Item1 * obj[it + 1].Item2;
            if (it < objects / 2 && res <= 0)   
            {
                Modify(templ, 1);
            }
            else if (it >= objects / 2 && res > 0)
            {
                Modify(templ, -1);
            }
            else
            {
                Modify(templ, 0);
            }
        }

        public void Modify(int[] pfunc, int p)
        {
            for (int i = 0; i < 4; i++)
            {
                func[i] += p * pfunc[i];
            }
            Console.WriteLine("{0} + {1}x1 + {2}x2 +{3}x1x2", pfunc[0], pfunc[1], pfunc[2], pfunc[3]);
        }
    }
}
