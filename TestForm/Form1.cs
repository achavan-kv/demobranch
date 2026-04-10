using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using TestForm.data;

namespace TestForm
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                string filePath = Path.Combine(Application.StartupPath, "data.json");

                string json = File.ReadAllText(filePath);

                Root data = JsonConvert.DeserializeObject<Root>(json);

                txtOutput.Clear();

                foreach (var student in data.students)
                {
                    txtOutput.AppendText(
                        $"ID: {student.id}, Name: {student.name}, Age: {student.age}"
                        + Environment.NewLine
                    );
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
            }
        }
    }
}
