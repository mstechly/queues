using System.ComponentModel;
using System.Diagnostics;
using QuickGraph;

namespace GraphSharpDemo.GraphBits
{
    /// <summary>
    /// A simple identifiable edge.
    /// </summary>
    [DebuggerDisplay("{Source.ID} -> {Target.ID}")]
    public class PocEdge : Edge<PocVertex>, INotifyPropertyChanged
    {
        private string id;

        public string ID
        {
            get { return id; }
            set
            {
                id = value;
                NotifyPropertyChanged("ID");
            }
        }

        public PocEdge(string id, PocVertex source, PocVertex target)
            : base(source, target)
        {
            ID = id;
        }

        public bool ShowTooltip => true;


        #region INotifyPropertyChanged Implementation

        public event PropertyChangedEventHandler PropertyChanged;

        private void NotifyPropertyChanged(string info)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new PropertyChangedEventArgs(info));
            }
        }

        #endregion
    }
}